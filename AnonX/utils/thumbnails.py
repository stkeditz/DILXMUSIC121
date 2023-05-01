from AnonX import app
import asyncio
import os

import re
import textwrap
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
from youtubesearchpython.__future__ import VideosSearch
import numpy as np

from config import YOUTUBE_IMG_URL


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


def truncate(text):
    list = text.split(" ")
    text1 = ""
    text2 = ""
    for i in list:
        if len(text1) + len(i) < 30:
            text1 += " " + i
        elif len(text2) + len(i) < 30:
            text2 += " " + i

    text1 = text1.strip()
    text2 = text2.strip()
    return [text1, text2]


async def gen_thumb(videoid, user_id):
    try:
        if os.path.isfile(f"cache/{videoid}_{user_id}.jpg"):
            return f"cache/{videoid}_{user_id}.jpg"

        url = f"https://www.youtube.com/watch?v={videoid}"
        if 1 == 1:
            results = VideosSearch(url, limit=1)
            for result in (await results.next())["result"]:
                try:
                    title = result["title"]
                    title = re.sub("\W+", " ", title)
                    title = title.title()
                except:
                    title = "Unsupported Title"
                try:
                    duration = result["duration"]
                except:
                    duration = "Unknown Mins"
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                try:
                    views = result["viewCount"]["short"]
                except:
                    views = "Unknown Views"
                try:
                    channel = result["channel"]["name"]
                except:
                    channel = "Unknown Channel"

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"http://img.youtube.com/vi/{videoid}/maxresdefault.jpg"
                ) as resp:
                    if resp.status == 200:
                        f = await aiofiles.open(f"cache/thumb{videoid}.jpg", mode="wb")
                        await f.write(await resp.read())
                        await f.close()

            wxyz = await app.get_profile_photos(user_id)
            try:
                wxy = await app.download_media(
                    wxyz[0]["file_id"], file_name=f"{user_id}.jpg"
                )
            except:
                hehe = await app.get_profile_photos(app.id)
                wxy = await app.download_media(
                    hehe[0]["file_id"], file_name=f"{app.id}.jpg"
                )
            xy = Image.open(wxy)

            a = Image.new("L", [640, 640], 0)
            b = ImageDraw.Draw(a)
            b.pieslice([(0, 0), (640, 640)], 0, 360, fill=255, outline="white")
            c = np.array(xy)
            d = np.array(a)
            e = np.dstack((c, d))
            f = Image.fromarray(e)
            x = f.resize((170, 170))

            youtube = Image.open(f"cache/thumb{videoid}.jpg")
            image1 = changeImageSize(1280, 720, youtube)
            image2 = image1.convert("RGBA")
            background = image2.filter(filter=ImageFilter.BoxBlur(30))
            enhancer = ImageEnhance.Brightness(background)
            background = enhancer.enhance(0.6)
            image2 = background

            circle = Image.open("AnonX/assets/circle.png")

            image3 = image1.crop((280, 0, 1000, 720))
            lum_img = Image.new("L", [720, 720], 0)
            draw = ImageDraw.Draw(lum_img)
            draw.pieslice([(0, 0), (720, 720)], 0, 360, fill=255, outline="white")
            img_arr = np.array(image3)
            lum_img_arr = np.array(lum_img)
            final_img_arr = np.dstack((img_arr, lum_img_arr))
            image3 = Image.fromarray(final_img_arr)
            image3 = image3.resize((600, 600))

            image2.paste(image3, (50, 70), mask=image3)
            image2.paste(x, (470, 490), mask=x)
            image2.paste(circle, (0, 0), mask=circle)

            # fonts
            font1 = ImageFont.truetype("AnonX/assets/font2.ttf", 30)
            font2 = ImageFont.truetype("AnonX/assets/font2.ttf", 70)
            font3 = ImageFont.truetype("AnonX/assets/font2.ttf", 40)
            font4 = ImageFont.truetype("AnonX/assets/font2.ttf", 35)

            image4 = ImageDraw.Draw(image2)
            image4.text(
                (10, 10), "Insane Music", fill="white", font=font1, align="left"
            )
            image4.text(
                (670, 150),
                "Now Playing",
                fill="white",
                font=font2,
                stroke_width=2,
                stroke_fill="white",
                align="left",
            )

            # title
            title1 = truncate(title)
            image4.text(
                (670, 300),
                text=title1[0],
                fill="white",
                stroke_width=1,
                stroke_fill="white",
                font=font3,
                align="left",
            )
            image4.text(
                (670, 350),
                text=title1[1],
                fill="white",
                stroke_width=1,
                stroke_fill="white",
                font=font3,
                align="left",
            )

            # description
            views = f"Views : {views}"
            duration = f"Duration : {duration} Mins"
            channel = f"Channel : {channel}"

            image4.text((670, 450), text=views, fill="white", font=font4, align="left")
            image4.text(
                (670, 500), text=duration, fill="white", font=font4, align="left"
            )
            image4.text(
                (670, 550), text=channel, fill="white", font=font4, align="left"
            )

            image2 = ImageOps.expand(image2)
            image2 = image2.convert("RGB")
            image2.save(f"cache/{videoid}_{user_id}.jpg")
            file = f"cache/{videoid}_{user_id}.jpg"
            return file
    except Exception as e:
        print(e)
        return YOUTUBE_IMG_URL


async def gen_qthumb(videoid, user_id):
    if os.path.isfile(f"cache/que{videoid}_{user_id}.png"):
        return f"cache/que{videoid}_{user_id}.png"
    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except:
                duration = "Unknown"
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            try:
                result["viewCount"]["short"]
            except:
                pass
            try:
                result["channel"]["name"]
            except:
                pass

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"cache/thumb{videoid}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()

        try:
            wxyz = await app.get_profile_photos(user_id)
            wxy = await app.download_media(wxyz[0]['file_id'], file_name=f'{user_id}.jpg')
        except:
            hehe = await app.get_profile_photos(app.id)
            wxy = await app.download_media(hehe[0]['file_id'], file_name=f'{app.id}.jpg')
        xy = Image.open(wxy)
        a = Image.new('L', [640, 640], 0)
        b = ImageDraw.Draw(a)
        b.pieslice([(0, 0), (640,640)], 0, 360, fill = 255, outline = "white")
        c = np.array(xy)
        d = np.array(a)
        e = np.dstack((c, d))
        f = Image.fromarray(e)
        x = f.resize((107, 107))

        youtube = Image.open(f"cache/thumb{videoid}.png")
        bg = Image.open(f"AnonX/assets/circle.png")
        image1 = changeImageSize(1280, 720, youtube)
        image2 = image1.convert("RGBA")
        background = image2.filter(filter=ImageFilter.BoxBlur(30))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.6)

        image3 = changeImageSize(1280, 720, bg)
        image5 = image3.convert("RGBA")
        Image.alpha_composite(background, image5).save(f"cache/temp{videoid}.png")

        Xcenter = youtube.width / 2
        Ycenter = youtube.height / 2
        x1 = Xcenter - 250
        y1 = Ycenter - 250
        x2 = Xcenter + 250
        y2 = Ycenter + 250
        logo = youtube.crop((x1, y1, x2, y2))
        logo.thumbnail((520, 520), Image.ANTIALIAS)
        logo.save(f"cache/chop{videoid}.png")
        if not os.path.isfile(f"cache/cropped{videoid}.png"):
            im = Image.open(f"cache/chop{videoid}.png").convert("RGBA")
            add_corners(im)
            im.save(f"cache/cropped{videoid}.png")

        crop_img = Image.open(f"cache/cropped{videoid}.png")
        logo = crop_img.convert("RGBA")
        logo.thumbnail((365, 365), Image.ANTIALIAS)
        width = int((1280 - 365) / 2)
        background = Image.open(f"cache/temp{videoid}.png")
        background.paste(logo, (width + 2, 138), mask=logo)
        background.paste(x, (710, 427), mask=x)
        background.paste(image3, (0, 0), mask=image3)

        draw = ImageDraw.Draw(background)
        font = ImageFont.truetype("AnonX/assets/font2.ttf", 45)
        ImageFont.truetype("AnonX/assets/font2.ttf", 70)
        arial = ImageFont.truetype("AnonX/assets/font2.ttf", 30)
        ImageFont.truetype("AnonX/assets/font.ttf", 30)
        para = textwrap.wrap(title, width=32)
        try:
            draw.text(
                (455, 25),
                "ADDED TO QUEUE",
                fill="white",
                stroke_width=5,
                stroke_fill="black",
                font=font,
            )
            if para[0]:
                text_w, text_h = draw.textsize(f"{para[0]}", font=font)
                draw.text(
                    ((1280 - text_w) / 2, 530),
                    f"{para[0]}",
                    fill="white",
                    stroke_width=1,
                    stroke_fill="white",
                    font=font,
                )
            if para[1]:
                text_w, text_h = draw.textsize(f"{para[1]}", font=font)
                draw.text(
                    ((1280 - text_w) / 2, 580),
                    f"{para[1]}",
                    fill="white",
                    stroke_width=1,
                    stroke_fill="white",
                    font=font,
                )
        except:
            pass
        text_w, text_h = draw.textsize(f"Duration: {duration} Mins", font=arial)
        draw.text(
            ((1280 - text_w) / 2, 660),
            f"Duration: {duration} Mins",
            fill="white",
            font=arial,
        )

        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass
        file = f"cache/que{videoid}_{user_id}.png"
        background.save(f"cache/que{videoid}_{user_id}.png")
        return f"cache/que{videoid}_{user_id}.png"
    except Exception as e:
        print(e)
        return YOUTUBE_IMG_URL
