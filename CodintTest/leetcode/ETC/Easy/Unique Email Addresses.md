### 소모 시간
- 14분

### 통과율
- 100%

### my solution
```
import re

class Solution:
    def numUniqueEmails(self, emails: List[str]) -> int:
        unique_emails = set()
        for email in emails:
            local, domain = email.split("@")
                        
            plus_index = local.find("+")
            
            # plus exists
            if plus_index != -1:
                local = local[:plus_index]
            
            local = re.sub("\.", "", local)
            
            unique_emails.add(local + "@" + domain)
        
        return len(unique_emails)
```

### other solution
- https://leetcode.com/problems/unique-email-addresses/discuss/186798/JavaPython-3-7-and-6-liners-with-comment-and-analysis.
```
def numUniqueEmails(self, emails: List[str]) -> int:
    seen = set()
    for email in emails:
        name, domain = email.split('@') 
        local = name.split('+')[0].replace('.', '')
        seen.add(local + '@' + domain)
    return len(seen)
```