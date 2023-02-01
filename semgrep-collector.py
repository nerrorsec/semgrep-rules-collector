import subprocess
import re 

user = "kali"

def collect_rules():
    subprocess.call(f"mkdir -p /home/{user}/semgrep-rules/", shell=True)
    rules_repo = ["https://github.com/returntocorp/semgrep-rules", "https://github.com/0xdea/semgrep-rules", "https://github.com/elttam/semgrep-rules", "https://github.com/trailofbits/semgrep-rules", "https://github.com/kondukto-io/semgrep-rules", "https://github.com/parsiya/semgrep-hotspots",
                  "https://github.com/ligurio/semgrep-rules", "https://github.com/federicodotta/semgrep-rules", "https://github.com/frappe/semgrep-rules", "https://github.com/dgryski/semgrep-go/blob/master/badnilguard.yml", "https://github.com/Decurity/semgrep-smart-contracts", "https://github.com/semgrep/rules-nodejsscan/tree/master/nodejsscan"]
    r = open('/tmp/rules_repo.enforce', 'a')
    for repo in rules_repo:
        save_at = re.findall(
            r'com/[a-zA-Z0-9_-]*/[a-zA-Z0-9_-]*', repo)[0].replace('com/', '')
        r.write(
            f'git clone {repo} /home/{user}/semgrep-rules/{save_at}\n')
    r.close()
    # download all rules
    subprocess.call(
        'interlace -threads 40 -cL /tmp/rules_repo.enforce -t nerrorsec', shell=True)
    # remove files that is not .yaml or .yml
    subprocess.call(
        f"find /home/{user}/semgrep-rules/ -type f -not \(-name '*.yaml' -o -name '*.yml' \) -print -delete", shell=True)
    # remove duplicates
    subprocess.call(
        f"fdupes -r /home/{user}/semgrep-rules/ -d -N", shell=True)
    # remove files that does not match rules syntax
    subprocess.call(f"grep -irlPzv '(?s)^rules.*id' /home/{user}/semgrep-rules/ | xargs rm -f", shell=True)
    # validate invalid rules
    subprocess.call(f"semgrep scan --validate --config=/home/{user}/semgrep-rules/ &> /tmp/rules.enforce.invalid", shell=True)
    # remove invalid rules
    subprocess.call(f"grep -iPoh '/home/{user}/semgrep-rules/.*\.(yaml|yml)' /tmp/rules.enforce.invalid | xargs rm -f", shell=True)
    # remove empty directories
    subprocess.call(f"find /home/{user}/semgrep-rules/ -empty -type d -delete", shell=True)
collect_rules()
# nerrorsec - NSL
