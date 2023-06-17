import requests

webhook_url = 'https://discord.com/api/webhooks/1119547326302793768/stcriwZkOBcVQlzGTwTpw415XPRirVkBdoE0b9sZF9u3Zi9n_QNG1RnLgTLbddVakq6v'

user_ids = [1752117, 25013944]

# Dictionary to store the previous presence state for each user
previous_presence = {}

def check_presence():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    data = {
        "userIds": user_ids
    }

    response = requests.post('https://presence.roblox.com/v1/presence/users', headers=headers, data=json.dumps(data))
    response_data = response.json()

    # Check if the response contains userPresences
    if "userPresences" in response_data:
        user_presences = response_data["userPresences"]

        # Check if userPresences list is not empty
        if user_presences:
            for user_presence in user_presences:
                user_id = user_presence.get("userId")
                user_presence_type = user_presence.get("userPresenceType")

                if user_presence_type is not None:
                    previous_state = previous_presence.get(user_id)
                    if previous_state is None:
                        # User is being tracked for the first time
                        previous_presence[user_id] = user_presence_type
                    else:
                        if previous_state == 0 and user_presence_type == 1:
                            # User went from offline to online
                            send_message(user_id)

                    previous_presence[user_id] = user_presence_type
                else:
                    print("User Presence Type not found in the response.")
        else:
            print("Empty userPresences list in the response.")
    else:
        print("userPresences not found in the response.")

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

def get_roblox_profile_url(user_id):
    return f"https://www.roblox.com/users/{user_id}/profile"

def get_rolimons_profile_url(user_id):
    return f"https://www.rolimons.com/player/{user_id}"

def send_message(user_id):
    username = get_roblox_username(user_id)
    data = {
    "embeds": [{
        "title": "A limited owner is online!",
        "color": 14548992,
        "description": f"**{username}** is now online! Check out their profile:",
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
            }
        ]
    }]
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code != 204:
        print(f"Failed to send Discord message. Error code: {response.status_code}")

send_message(1752117)
