# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


def remove_slash(value):
    return value.replace("\\", "").strip()


class WrestlingterritoriesItem(scrapy.Item):
    # define the fields for your item here like:
    Wrestler = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Currentgimmick = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Age = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Promotion = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Brand = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Birthplace = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Gender = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Height = scrapy.Field(input_processor=MapCompose(
        remove_tags, remove_slash), output_processor=TakeFirst())
    Weight = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Backgroundinsports = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    SocialMedia = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Alteregos = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Roles = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Beginningofinringcareer = scrapy.Field(
        input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    Endofinringcareer = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Inringexperience = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Wrestlingstyle = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Trainer = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Nicknames = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Signaturemoves = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    ActiveRoles = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
