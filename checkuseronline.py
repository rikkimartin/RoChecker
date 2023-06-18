import json
import time
import requests

webhook_url = 'https://discord.com/api/webhooks/1119547326302793768/stcriwZkOBcVQlzGTwTpw415XPRirVkBdoE0b9sZF9u3Zi9n_QNG1RnLgTLbddVakq6v'

#Currently loading SKOTN
owner_url = "https://inventory.roblox.com/v2/assets/439945661/owners"

# List of all user_ids
# user_ids = [1752117, 25013944] deprecated for testing reasons
user_ids = []

# Dict to check previous state
my_dict = {}

# Infinite loop ran to continuously check all the players' presence in the user_ids list
def monitor_players():
    print("Starting online checker...")
    while True:
        #print("Loop")
        check_presence()
        time.sleep(30)

def check_presence():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Cookie': '.ROBLOSECURITY=_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_B5B9BCFFDC07B97884ADB97803A43BBABF22858BBD53FFEB2C87D0A330A0F9216073ADA0C4BA01CE17CB84A261DE621853C4809561B55D201F0D303D5615B7CF034B35A99189B0E7CA1E31581EE571E237E692E97BBB0520C8DF293F16AEA3ED6796B3024591DB3EA3746829E137D76F9AD2BB90B1AA2246BB94F39112790AB2C8FF74D6E5A2C3261C90539F35377C018FC27427624546FE409E2037E4515CE746635B3F9F7EF2BB6073905417E057E0BC00F3EE5F75715234A4DDB0566AF73A8F181417FC8308F2F01B729CCDEB676EE7BB04D22E8F0D3B06D96D667C7723D90873A0B7677860210E0E3E37FAB4E121CB7B7A71C0F6E8C2A2297958EBBD197B578170C152174E2C144D0F31AF222D4504B9189F4CB06D7D2165EC46809694C565591C7E38D68C3EDC2DB2C1F5E0155B1AF343A914F91C52C7A2018D4FAE9903CDA06A218830CD6106EE5EAD674F78E00146196786F5C09ED8207018C5E381E5CA50DA33C03E81247334F90B5C7245B9DC21734E'
    }

    data = {
        "userIds": user_ids
    }

    response = requests.post('https://presence.roblox.com/v1/presence/users', headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_data = response.json()
        presence_data = response_data.get("userPresences", [])
        if presence_data:
            for presence in presence_data:
                isOnline = presence.get("userPresenceType") 
                userID = presence.get("userId")
                placeID = presence.get("placeId")
                print(userID)
                print(placeID)
                previous_state = my_dict.get(userID) 
                if previous_state != 2 and isOnline == 2:
                    send_message(userID,placeID)
                my_dict[userID] = isOnline
        else:
            print("No presence data found")
    else:
        print("Post request failed.")

# Retrieves a player's roblox username through RobloxAPI, with user_id as param
def get_roblox_username(user_id):
    url = f"https://users.roblox.com/v1/users/{user_id}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        username = data.get("name")
        if username:
            return username
        else:
            print("Username not found in the response.")
    else:
        print(f"Failed to fetch username. Status code: {response.status_code}")

    return None

# Retrieves a player's roblox avatar imageURL through RobloxAPI, with user_id as param
def get_avatar_image(user_id):
    url = f"https://thumbnails.roblox.com/v1/users/avatar?userIds={user_id}&size=420x420&format=Png&isCircular=false"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        avatar_data = data.get("data", [])
        if avatar_data:
            avatar_url = avatar_data[0].get("imageUrl")
            return avatar_url
        else:
            print("Avatar data not found in the response.")
    else:
        print(f"Failed to fetch avatar url. Status code: {response.status_code}")

    return None

# Retrieves a player's roblox profile url in string
def get_roblox_profile_url(user_id):
    return f"https://www.roblox.com/users/{user_id}/profile"

# Retrieves a player's rolimons_profile_url in string
def get_rolimons_profile_url(user_id):
    return f"https://www.rolimons.com/player/{user_id}"

def get_place_id(placeID):
    if placeID > 0:
        return f"https://www.roblox.com/games/{placeID}/"
    else:
        return "Follows are off"
        

# Embeds a message that is send through the discord webhook with all of a player's information. Communicates through a post request on DiscordAPI webhook url.
def send_message(user_id, place_id):
    username = get_roblox_username(user_id)
    data = {
    "embeds": [{
        "title": "A limited owner is in-game!",
        "color": 14548992,
        "description": f"**{username}** is now in-game! Check out their profile:",
        "image": {
            "url": get_avatar_image(user_id)
        },
        "fields": [
            {
                "name": "Roblox Profile",
                "value": get_roblox_profile_url(user_id),
                "inline": True
            },
            {
                "name": "Rolimons Profile",
                "value": get_rolimons_profile_url(user_id),
                "inline": True
            },
            {
                "name": "Game Link",
                "value": get_place_id(place_id),
                "inline": True
            }
        ]
    }]
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code != 204:
        print(f"Failed to send Discord message. Error code: {response.status_code}")

def load_owners():
    ownerHeader = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Cookie': '.ROBLOSECURITY=_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_B5B9BCFFDC07B97884ADB97803A43BBABF22858BBD53FFEB2C87D0A330A0F9216073ADA0C4BA01CE17CB84A261DE621853C4809561B55D201F0D303D5615B7CF034B35A99189B0E7CA1E31581EE571E237E692E97BBB0520C8DF293F16AEA3ED6796B3024591DB3EA3746829E137D76F9AD2BB90B1AA2246BB94F39112790AB2C8FF74D6E5A2C3261C90539F35377C018FC27427624546FE409E2037E4515CE746635B3F9F7EF2BB6073905417E057E0BC00F3EE5F75715234A4DDB0566AF73A8F181417FC8308F2F01B729CCDEB676EE7BB04D22E8F0D3B06D96D667C7723D90873A0B7677860210E0E3E37FAB4E121CB7B7A71C0F6E8C2A2297958EBBD197B578170C152174E2C144D0F31AF222D4504B9189F4CB06D7D2165EC46809694C565591C7E38D68C3EDC2DB2C1F5E0155B1AF343A914F91C52C7A2018D4FAE9903CDA06A218830CD6106EE5EAD674F78E00146196786F5C09ED8207018C5E381E5CA50DA33C03E81247334F90B5C7245B9DC21734E'
    }

    response = requests.get(owner_url, headers=ownerHeader, params={"limit": 100, "sortOrder": "Asc"})
    data = response.json()

    for item in data["data"]:
        if item is not None and item.get("owner") is not None and item.get("updated") is not None:
            if item["updated"] < "2021-01-01T00:00:00.000Z":
                user_ids.append(item["owner"]["id"])

    next_page_cursor = data.get("nextPageCursor")

    while next_page_cursor:
        params = {"limit": 100, "sortOrder": "Asc", "cursor": next_page_cursor}
        response = requests.get(owner_url, headers=ownerHeader, params=params)
        data = response.json()

        for item in data["data"]:
            if item is not None and item.get("owner") is not None and item.get("updated") is not None:
                if item["updated"] < "2021-01-01T00:00:00.000Z":
                    user_ids.append(item["owner"]["id"])

        next_page_cursor = data["nextPageCursor"]
        
        message_one = "Loaded -> "
        owner_count = len(user_ids)
        message_two = " <- lim owners into list"
        result = message_one + str(owner_count) + message_two
        print(result)



load_owners()
monitor_players()
