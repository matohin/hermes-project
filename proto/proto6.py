import sys
import json
import logging

import requests
import msal

config = {
    'authority': 'https://login.microsoftonline.com/common',
    'client_id': '5fbf6ac1-437f-4ea3-a64b-e8c3287bff57',
    # 'scope1': 'https://graph.microsoft.com/.default',
    'scope1': 'https://graph.microsoft.com/.default',
    'scope2': ['Tasks.ReadWrite'], #, 'User.Read'
    # 'scope2': ["https://graph.microsoft.com/user.read"],
    'secret': 'XhP~_76-1~h_3owuUS_Q74ot4m2NsFPy3~',
}

# code = None
# code='M.R3_BAY.1bc52a0a-d1fe-d0b9-8d6b-cebfeab94c27'

app = msal.ConfidentialClientApplication(
    config["client_id"], authority=config["authority"],
    client_credential=config["secret"])

result1 = app.acquire_token_for_client(config['scope1'])

# print(result1)

at = "EwBoA8l6BAAU6k7+XVQzkGyMv7VHB/h4cHbJYRAAAeEKj+4QW7LsrhCiMLVM8ri/YzGRsEnKcunupu05PcxepFxEVo8BnpTkAX9gvSj+rvqLXa5YCRmM1JAsn8R8ueGxkaGP8hhOCA1lTnRjufwGFREnENBAc3XD+1BeW2CfrmfcH1zmROaQszHXiypUXGCGwyfEHbcoF5hvmuuVe/Xnij13cp/8q+vP/FsoeNLxzOxXjW2YlucVgepBbbKwrMCDSi5X/CKj4Gtg+jjgJOh71DWl6sag7UOJMMYNBiVgMsahhuWPc3rO9xNbH6PUct+nLfGegFf6w7cK65XlcDrYa31x8Ai+b8JtXk98VwGbcI4WxveDTVXNybKP3vNlTk4DZgAACEnYhOJc+BK3OAJxNdQIprgZn53YUUTaEPGCbLuOzAh4xDiGKzM98daFukP2hDmjF5js71wHusjVYhC5ZKlWM6uMI+eB6thi10s2IqIF0YMZpPTH+4SI57JeI40bn+ecgqJb/bjT2aE4vDm0J5Q11VpVivpk6uiGwNn/rWsbBlGsZ2zo3Bpb1cu5k9gO4Ad5SS6jDG81Pq3Zk+zS76Mt9++ZENMi+blnZuUJzWNSmr5n8eEGINrl5PmJ7lPkzIy41WkOWH5lO+BfmArvfqVgNAB4xuCD6gGxAciQQ90SvDm4de9Y8HU2iT2GMllvsvO0BpFZzjBXJxdnyPW9O2uu7X0r+421VnYJoLfMyzNI7Uu6w4zgjSWRvKXXd2XQLUXW1WwA+9wAz8bquvV4bKBT6Qg8nxZ/2RaQ4vofR8RB7q2xXk3/iJI/fykK46Pl1KX3fXyqD3kPh9s9myQnZKkDHugD9+jFt6S9PsyjolgeHTUTw83jgJfftoiBx4P6MXzpc2J3l4/am4/X6M/rHUt2LLN8/U1dZ+jGp0WS6d4Y0Z/svHU+yXBpbD/nC5m4c7TN07zlt2x6wudLN7z0STB0GqyXRc4YiGerVINyhpBLhNV6nVR99NxPc9RhCL5ZIgUFH3KSJf/3wZV1ikV30Er4pWd12xEn9/G8BLTthGzKR8VCSt9X/zzX7pdb1j1cLg+6aNk061+H+pNErxNnWLnH847e+oBxWYYIIIy75ppw2iTD9n634qdG5CQXoIeD6GGolUJ6agI=', 'refresh_token': 'M.R3_BAY.CatIDkggGgNpG7nVgXnkCraAK0!gqT0iLKO1v38C11ZCbPVNdWHoRi*v1HnqOfxdz4rNchwt*Hz6tOFvqMMVaMrOQN2wGeBet2jtaAuMv7WAn33MiYrnnd36kkmJwDsVe1Rbo0T2T5*DUBcc*2hT1AY2lpvTebvspwCQpYKXgHZbmBvMTtiv*5EpUDvTDLxsIdZ9qo6czjotXIAQVRZ289U*ST3JS0h2O!494mRbxtx!S4ZbmKjPSm4VEzIVH!A8JVyvTBDklbu9hN272O5MaMriN4j2yxnMrdKjnDwtpA18Ed699b4X8lpBzi3L9Cxu7!ArovmVoJFNpaMtsnEPKRn7U3FZhy2rkpV7tHl7HnYdP*RHIuDwMEX7IV6qaQpxixPqvxcChhZZz2yj2rND0stOL5kkMMB9dgs3RyXtcgQnd7VpNXfmWOe3m8IjO6owAbMnyiJRwqByz0mh3Ytw!RM$', 'id_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjFMVE16YWtpaGlSbGFfOHoyQkVKVlhlV01xbyJ9.eyJ2ZXIiOiIyLjAiLCJpc3MiOiJodHRwczovL2xvZ2luLm1pY3Jvc29mdG9ubGluZS5jb20vOTE4ODA0MGQtNmM2Ny00YzViLWIxMTItMzZhMzA0YjY2ZGFkL3YyLjAiLCJzdWIiOiJBQUFBQUFBQUFBQUFBQUFBQUFBQUFKeUVQeVE5VUtCb0w5bDhoWE5Vek9JIiwiYXVkIjoiNWZiZjZhYzEtNDM3Zi00ZWEzLWE2NGItZThjMzI4N2JmZjU3IiwiZXhwIjoxNjE1NDA3NjE2LCJpYXQiOjE2MTUzMjA5MTYsIm5iZiI6MTYxNTMyMDkxNiwibmFtZSI6IkV2Z2VuaXkgTWF0b2hpbiIsInByZWZlcnJlZF91c2VybmFtZSI6Im1hdG9oaW5AbXNuLmNvbSIsIm9pZCI6IjAwMDAwMDAwLTAwMDAtMDAwMC1lNjcyLTFkOGFkNTI2Yzc0MSIsInRpZCI6IjkxODgwNDBkLTZjNjctNGM1Yi1iMTEyLTM2YTMwNGI2NmRhZCIsImFpbyI6IkRYSFp2Vlh4WkcqeFdSMkpDN3p6Wm1NRU9TNGVQZzYwVTZpSVRRRW5sSEtSR0RXMXBVaipxMkJ2cFhSIWZjUXVMMVFnQ00qNnZTcnchbVFRR1ZBUlJFdDNoRjchKlRrSnB3ZXZjVnZuTlhJSFduWnpZYzVQQUd2dXJQb21ZZmlaKkExY2p6NyFTT1hLdG1PWSE2UVBQa00kIn0.uCMmwBm1k83H8FY87SmCLKeeJQktpI4o_3X-0O_1kVCmxdWpUh_2EySKKR5iFFV1zKaEhGGr41tu20u_XzvCK1LMSd0nt8dY1pRX-ZNiUeDWc4YOjU2OaalQoECCX6dMUUeXQVr-2E2dpL3iTJBaKKkba5VK4lleSFFFGpF9SjhRkJA4Cf3OiNxiFuLvcNigHix7jhNNjuboJkgJ5MrlJ51-EyPFn7Ft4wY8B9yX1-boCn5iM3ilEo_bO3Q0CescB_b42wlKY9LGft5aXWyYH2EoNC-JFGwGNhwVV7FMPIdjgiWXj6J2quCdzKlkkNcgkDY_MGxh9_wHI2d2PA7LcQ', 'client_info': 'eyJ2ZXIiOiIxLjAiLCJzdWIiOiJBQUFBQUFBQUFBQUFBQUFBQUFBQUFKeUVQeVE5VUtCb0w5bDhoWE5Vek9JIiwibmFtZSI6IkV2Z2VuaXkgTWF0b2hpbiIsInByZWZlcnJlZF91c2VybmFtZSI6Im1hdG9oaW5AbXNuLmNvbSIsIm9pZCI6IjAwMDAwMDAwLTAwMDAtMDAwMC1lNjcyLTFkOGFkNTI2Yzc0MSIsInRpZCI6IjkxODgwNDBkLTZjNjctNGM1Yi1iMTEyLTM2YTMwNGI2NmRhZCIsImhvbWVfb2lkIjoiMDAwMDAwMDAtMDAwMC0wMDAwLWU2NzItMWQ4YWQ1MjZjNzQxIiwidWlkIjoiMDAwMDAwMDAtMDAwMC0wMDAwLWU2NzItMWQ4YWQ1MjZjNzQxIiwidXRpZCI6IjkxODgwNDBkLTZjNjctNGM1Yi1iMTEyLTM2YTMwNGI2NmRhZCJ9"
result2 = app.acquire_token_on_behalf_of(user_assertion=at , scopes=config['scope2'])

print(result2)
