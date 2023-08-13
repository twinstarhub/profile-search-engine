async def scrape_discord_profiles(start_user_id, num_profiles):
    profiles = []
    
    for i in range(start_user_id, start_user_id + num_profiles):
        user_id = str(i)
        profile_url = f"https://discord.com/users/{user_id}"  # Fix the URL format
        async with aiohttp.ClientSession() as session:
            async with session.get(profile_url) as response:
                if response.status == 200:
                    content = await response.text()
                    soup = BeautifulSoup(content, "html.parser")
                    username_element = soup.select_one(".username")

                    if username_element is not None:
                        username = username_element.text.strip()
                        discriminator = soup.select_one(".discriminator").text.strip()
                        avatar_url = soup.select_one(".avatar").get("src")
                        profiles.append({
                            "User ID": user_id,
                            "Username": username,
                            "Discriminator": discriminator,
                            "Avatar URL": avatar_url
                        })
                    else:
                        print(f"User isn't found: {user_id}")
                else:
                    print(f"Failed to get the user's profile: {user_id}")

    return profiles