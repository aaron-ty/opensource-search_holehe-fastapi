from holehe.modules.cms.atlassian import atlassian
from holehe.modules.cms.gravatar import gravatar
from holehe.modules.cms.voxmedia import voxmedia
from holehe.modules.cms.wordpress import wordpress
from holehe.modules.company.aboutme import aboutme
from holehe.modules.crm.amocrm import amocrm
from holehe.modules.crm.axonaut import axonaut
from holehe.modules.crm.hubspot import hubspot
from holehe.modules.crm.insightly import insightly
from holehe.modules.crm.nimble import nimble
from holehe.modules.crm.nocrm import nocrm
from holehe.modules.crm.nutshell import nutshell
from holehe.modules.crm.pipedrive import pipedrive
from holehe.modules.crm.teamleader import teamleader
from holehe.modules.crm.zoho import zoho
from holehe.modules.crowfunding.buymeacoffee import buymeacoffee
from holehe.modules.forum.babeshows import babeshows
from holehe.modules.forum.badeggsonline import badeggsonline
from holehe.modules.forum.biosmods import biosmods
from holehe.modules.forum.biotechnologyforums import biotechnologyforums
from holehe.modules.forum.blackworldforum import blackworldforum
from holehe.modules.forum.blitzortung import blitzortung
from holehe.modules.forum.bluegrassrivals import bluegrassrivals
from holehe.modules.forum.cambridgemt import cambridgemt
from holehe.modules.forum.chinaphonearena import chinaphonearena
from holehe.modules.forum.clashfarmer import clashfarmer
from holehe.modules.forum.codeigniter import codeigniter
from holehe.modules.forum.cpaelites import cpaelites
from holehe.modules.forum.cpahero import cpahero
from holehe.modules.forum.cracked_to import cracked_to
from holehe.modules.forum.demonforums import demonforums
from holehe.modules.forum.freiberg import freiberg
from holehe.modules.forum.koditv import koditv
from holehe.modules.forum.mybb import mybb
from holehe.modules.forum.nattyornot import nattyornot
from holehe.modules.forum.ndemiccreations import ndemiccreations
from holehe.modules.forum.nextpvr import nextpvr
from holehe.modules.forum.onlinesequencer import onlinesequencer
from holehe.modules.forum.thecardboard import thecardboard
from holehe.modules.forum.therianguide import therianguide
from holehe.modules.forum.thevapingforum import thevapingforum
from holehe.modules.jobs.coroflot import coroflot
from holehe.modules.jobs.freelancer import freelancer
from holehe.modules.jobs.seoclerks import seoclerks
from holehe.modules.learning.diigo import diigo
from holehe.modules.learning.duolingo import duolingo
from holehe.modules.learning.quora import quora
from holehe.modules.mails.google import google
from holehe.modules.mails.laposte import laposte
from holehe.modules.mails.mail_ru import mail_ru
from holehe.modules.mails.protonmail import protonmail
from holehe.modules.mails.yahoo import yahoo
from holehe.modules.medias.ello import ello
from holehe.modules.medias.flickr import flickr
from holehe.modules.medias.komoot import komoot
from holehe.modules.medias.rambler import rambler
from holehe.modules.medias.sporcle import sporcle
from holehe.modules.medical.caringbridge import caringbridge
from holehe.modules.medical.sevencups import sevencups
from holehe.modules.music.blip import blip
from holehe.modules.music.lastfm import lastfm
from holehe.modules.music.smule import smule
from holehe.modules.music.soundcloud import soundcloud
from holehe.modules.music.spotify import spotify
from holehe.modules.music.tunefind import tunefind
from holehe.modules.osint.rocketreach import rocketreach
from holehe.modules.payment.venmo import venmo
from holehe.modules.porn.pornhub import pornhub
from holehe.modules.porn.redtube import redtube
from holehe.modules.porn.xnxx import xnxx
from holehe.modules.porn.xvideos import xvideos
from holehe.modules.productivity.anydo import anydo
from holehe.modules.productivity.evernote import evernote
from holehe.modules.products.eventbrite import eventbrite
from holehe.modules.products.nike import nike
from holehe.modules.products.samsung import samsung
from holehe.modules.programing.codecademy import codecademy
from holehe.modules.programing.codepen import codepen
from holehe.modules.programing.devrant import devrant
from holehe.modules.programing.github import github
from holehe.modules.programing.replit import replit
from holehe.modules.programing.teamtreehouse import teamtreehouse
from holehe.modules.real_estate.vrbo import vrbo
from holehe.modules.shopping.amazon import amazon
from holehe.modules.shopping.armurerieauxerre import armurerieauxerre
from holehe.modules.shopping.deliveroo import deliveroo
from holehe.modules.shopping.dominosfr import dominosfr
from holehe.modules.shopping.ebay import ebay
from holehe.modules.shopping.envato import envato
from holehe.modules.shopping.garmin import garmin
from holehe.modules.shopping.naturabuy import naturabuy
from holehe.modules.shopping.vivino import vivino
from holehe.modules.social_media.bitmoji import bitmoji
from holehe.modules.social_media.crevado import crevado
from holehe.modules.social_media.discord import discord
from holehe.modules.social_media.facebook import facebook
from holehe.modules.social_media.fanpop import fanpop
from holehe.modules.social_media.imgur import imgur
from holehe.modules.social_media.instagram import instagram
from holehe.modules.social_media.myspace import myspace
from holehe.modules.social_media.odnoklassniki import odnoklassniki
from holehe.modules.social_media.parler import parler
from holehe.modules.social_media.patreon import patreon
from holehe.modules.social_media.pinterest import pinterest
from holehe.modules.social_media.plurk import plurk
from holehe.modules.social_media.snapchat import snapchat
from holehe.modules.social_media.strava import strava
from holehe.modules.social_media.taringa import taringa
from holehe.modules.social_media.tellonym import tellonym
from holehe.modules.social_media.tumblr import tumblr
from holehe.modules.social_media.twitter import twitter
from holehe.modules.social_media.vsco import vsco
from holehe.modules.social_media.wattpad import wattpad
from holehe.modules.social_media.xing import xing
from holehe.modules.software.adobe import adobe
from holehe.modules.software.archive import archive
from holehe.modules.software.docker import docker
from holehe.modules.software.firefox import firefox
from holehe.modules.software.issuu import issuu
from holehe.modules.software.lastpass import lastpass
from holehe.modules.software.office365 import office365
from holehe.modules.sport.bodybuilding import bodybuilding
from holehe.modules.transport.blablacar import blablacar
from pydash import get
from src.infrastructure.modules.requests_logic import (
    RequestBaseParamsAsync,
    RequestBaseParamsCFFIAsync,
    RequestBaseParamsH2,
)

module_mapping = {
    "aboutme": {
        "func": aboutme,
        "active": False,
        "description": "about.me",
        "method": "register",
        "client": {"request_class": RequestBaseParamsAsync, "use_proxy": True},
    },
    "adobe": {
        "func": adobe,
        "active": True,
        "description": "adobe.com",
        "method": "password recovery",
        "client": {
            "request_class": RequestBaseParamsH2,
            "use_proxy": True,
            "proxy_group": "1",
            "proxy_group_fallback": "5",
        },
    },
    "amazon": {
        "func": amazon,
        "active": True,
        "description": "amazon.com",
        "method": "login",
    },
    "amocrm": {
        "func": amocrm,
        "active": False,
        "description": "amocrm.com",
        "method": "register",
    },
    "anydo": {
        "func": anydo,
        "active": True,
        "description": "any.do",
        "method": "login",
    },
    "archive": {
        "func": archive,
        "active": True,
        "description": "archive.org",
        "method": "register",
    },
    "armurerieauxerre": {
        "func": armurerieauxerre,
        "active": True,
        "description": "armurerie-auxerre.com",
        "method": "register",
    },
    "atlassian": {
        "func": atlassian,
        "active": False,
        "description": "atlassian.com",
        "method": "register",
    },
    "axonaut": {
        "func": axonaut,
        "active": False,
        "description": "axonaut.com",
        "method": "register",
    },
    "babeshows": {
        "func": babeshows,
        "active": True,
        "description": "babeshows.co.uk",
        "method": "register",
    },
    "badeggsonline": {
        "func": badeggsonline,
        "active": False,
        "description": "badeggsonline.com",
        "method": "register",
    },
    "biosmods": {
        "func": biosmods,
        "active": True,
        "description": "bios-mods.com",
        "method": "register",
    },
    "biotechnologyforums": {
        "func": biotechnologyforums,
        "active": True,
        "description": "biotechnologyforums.com",
        "method": "register",
    },
    "bitmoji": {
        "func": bitmoji,
        "active": False,
        "description": "bitmoji.com",
        "method": "login",
    },
    "blablacar": {
        "func": blablacar,
        "active": False,
        "description": "blablacar.com",
        "method": "register",
    },
    "blackworldforum": {
        "func": blackworldforum,
        "active": False,
        "description": "blackworldforum.com",
        "method": "register",
    },
    "blip": {
        "func": blip,
        "active": True,
        "description": "blip.fm",
        "method": "register",
        "client": {"request_class": RequestBaseParamsAsync, "use_proxy": True},
    },
    "blitzortung": {
        "func": blitzortung,
        "active": True,
        "description": "forum.blitzortung.org",
        "method": "register",
    },
    "bluegrassrivals": {
        "func": bluegrassrivals,
        "active": True,
        "description": "bluegrassrivals.com",
        "method": "register",
    },
    "bodybuilding": {
        "func": bodybuilding,
        "active": False,
        "description": "bodybuilding.com",
        "method": "register",
    },
    "buymeacoffee": {
        "func": buymeacoffee,
        "active": False,
        "description": "buymeacoffee.com",
        "method": "register",
    },
    "cambridgemt": {
        "func": cambridgemt,
        "active": True,
        "description": "discussion.cambridge-mt.com",
        "method": "register",
    },
    "caringbridge": {
        "func": caringbridge,
        "active": False,
        "description": "caringbridge.org",
        "method": "register",
    },
    "chinaphonearena": {
        "func": chinaphonearena,
        "active": True,
        "description": "chinaphonearena.com",
        "method": "register",
    },
    "clashfarmer": {
        "func": clashfarmer,
        "active": True,
        "description": "clashfarmer.com",
        "method": "register",
        "client": {"request_class": RequestBaseParamsAsync, "use_proxy": True},
    },
    "codecademy": {
        "func": codecademy,
        "active": True,
        "description": "codecademy.com",
        "method": "register",
        "client": {"request_class": RequestBaseParamsAsync, "use_proxy": True},
    },
    "codeigniter": {
        "func": codeigniter,
        "active": True,
        "description": "forum.codeigniter.com",
        "method": "register",
    },
    "codepen": {
        "func": codepen,
        "active": False,
        "description": "codepen.io",
        "method": "register",
    },
    "coroflot": {
        "func": coroflot,
        "active": True,
        "description": "coroflot.com",
        "method": "register",
    },
    "cpaelites": {
        "func": cpaelites,
        "active": False,
        "description": "cpaelites.com",
        "method": "register",
    },
    "cpahero": {
        "func": cpahero,
        "active": False,
        "description": "cpahero.com",
        "method": "register",
    },
    "cracked_to": {
        "func": cracked_to,
        "active": False,
        "description": "cracked.to",
        "method": "register",
    },
    "crevado": {
        "func": crevado,
        "active": False,
        "description": "crevado.com",
        "method": "register",
        "client": {"request_class": RequestBaseParamsAsync, "use_proxy": True},
    },
    "deliveroo": {
        "func": deliveroo,
        "active": False,
        "description": "deliveroo.com",
        "method": "register",
    },
    "demonforums": {
        "func": demonforums,
        "active": True,
        "description": "demonforums.net",
        "method": "register",
        "client": {"request_class": RequestBaseParamsAsync, "use_proxy": True},
    },
    "devrant": {
        "func": devrant,
        "active": True,
        "description": "devrant.com",
        "method": "register",
    },
    "diigo": {
        "func": diigo,
        "active": False,
        "description": "diigo.com",
        "method": "register",
    },
    "discord": {
        "func": discord,
        "active": True,
        "description": "discord.com",
        "method": "register",
    },
    "docker": {
        "func": docker,
        "active": True,
        "description": "docker.com",
        "method": "register",
    },
    "dominosfr": {
        "func": dominosfr,
        "active": False,
        "description": "dominos.fr",
        "method": "register",
    },
    "duolingo": {
        "func": duolingo,
        "active": True,
        "description": "duolingo.com",
        "method": "other",
    },
    "ebay": {
        "func": ebay,
        "active": False,
        "description": "ebay.com",
        "method": "login",
    },
    "ello": {
        "func": ello,
        "active": False,
        "description": "ello.co",
        "method": "register",
    },
    "envato": {
        "func": envato,
        "active": True,
        "description": "envato.com",
        "method": "register",
    },
    "eventbrite": {
        "func": eventbrite,
        "active": False,
        "description": "eventbrite.com",
        "method": "login",
    },
    "evernote": {
        "func": evernote,
        "active": False,
        "description": "evernote.com",
        "method": "login",
    },
    "facebook": {
        "func": facebook,
        "active": False,
        "description": "facebook.com",
        "method": "register",
    },
    "fanpop": {
        "func": fanpop,
        "active": True,
        "description": "fanpop.com",
        "method": "register",
    },
    "firefox": {
        "func": firefox,
        "active": True,
        "description": "firefox.com",
        "method": "register",
    },
    "flickr": {
        "func": flickr,
        "active": True,
        "description": "flickr.com",
        "method": "login",
    },
    "freelancer": {
        "func": freelancer,
        "active": True,
        "description": "freelancer.com",
        "method": "register",
    },
    "freiberg": {
        "func": freiberg,
        "active": True,
        "description": "drachenhort.user.stunet.tu-freiberg.de",
        "method": "register",
    },
    "garmin": {
        "func": garmin,
        "active": False,
        "description": "garmin.com",
        "method": "register",
    },
    "github": {
        "func": github,
        "active": False,
        "description": "github.com",
        "method": "register",
    },
    "google": {
        "func": google,
        "active": False,
        "description": "google.com",
        "method": "register",
    },
    "gravatar": {
        "func": gravatar,
        "active": True,
        "description": "gravatar.com",
        "method": "other",
    },
    "hubspot": {
        "func": hubspot,
        "active": True,
        "description": "hubspot.com",
        "method": "login",
    },
    "imgur": {
        "func": imgur,
        "active": True,
        "description": "imgur.com",
        "method": "register",
        "client": {"request_class": RequestBaseParamsAsync, "use_proxy": True},
    },
    "insightly": {
        "func": insightly,
        "active": False,
        "description": "insightly.com",
        "method": "login",
    },
    "instagram": {
        "func": instagram,
        "active": False,
        "description": "instagram.com",
        "method": "register",
    },
    "issuu": {
        "func": issuu,
        "active": False,
        "description": "issuu.com",
        "method": "register",
    },
    "koditv": {
        "func": koditv,
        "active": True,
        "description": "forum.kodi.tv",
        "method": "register",
    },
    "komoot": {
        "func": komoot,
        "active": True,
        "description": "komoot.com",
        "method": "register",
        "client": {"request_class": RequestBaseParamsAsync, "use_proxy": True},
    },
    "laposte": {
        "func": laposte,
        "active": True,
        "description": "laposte.fr",
        "method": "register",
    },
    "lastfm": {
        "func": lastfm,
        "active": True,
        "description": "last.fm",
        "method": "register",
    },
    "lastpass": {
        "func": lastpass,
        "active": True,
        "description": "lastpass.com",
        "method": "register",
    },
    "mail_ru": {
        "func": mail_ru,
        "active": True,
        "description": "mail.ru",
        "method": "password recovery",
    },
    "mybb": {
        "func": mybb,
        "active": True,
        "description": "community.mybb.com",
        "method": "register",
    },
    "myspace": {
        "func": myspace,
        "active": False,
        "description": "myspace.com",
        "method": "register",
    },
    "nattyornot": {
        "func": nattyornot,
        "active": False,
        "description": "nattyornotforum.nattyornot.com",
        "method": "register",
    },
    "naturabuy": {
        "func": naturabuy,
        "active": True,
        "description": "naturabuy.fr",
        "method": "register",
    },
    "ndemiccreations": {
        "func": ndemiccreations,
        "active": True,
        "description": "forum.ndemiccreations.com",
        "method": "register",
    },
    "nextpvr": {
        "func": nextpvr,
        "active": True,
        "description": "forums.nextpvr.com",
        "method": "register",
    },
    "nike": {
        "func": nike,
        "active": False,
        "description": "nike.com",
        "method": "register",
    },
    "nimble": {
        "func": nimble,
        "active": False,
        "description": "nimble.com",
        "method": "register",
    },
    "nocrm": {
        "func": nocrm,
        "active": False,
        "description": "nocrm.io",
        "method": "register",
    },
    "nutshell": {
        "func": nutshell,
        "active": False,
        "description": "nutshell.com",
        "method": "register",
    },
    "odnoklassniki": {
        "func": odnoklassniki,
        "active": True,
        "description": "ok.ru",
        "method": "password recovery",
    },
    "office365": {
        "func": office365,
        "active": False,
        "description": "office365.com",
        "method": "other",
    },
    "onlinesequencer": {
        "func": onlinesequencer,
        "active": False,
        "description": "onlinesequencer.net",
        "method": "register",
    },
    "parler": {
        "func": parler,
        "active": True,
        "description": "parler.com",
        "method": "login",
    },
    "patreon": {
        "func": patreon,
        "active": False,
        "description": "patreon.com",
        "method": "login",
    },
    "pinterest": {
        "func": pinterest,
        "active": True,
        "description": "pinterest.com",
        "method": "register",
    },
    "pipedrive": {
        "func": pipedrive,
        "active": False,
        "description": "pipedrive.com",
        "method": "register",
    },
    "plurk": {
        "func": plurk,
        "active": True,
        "description": "plurk.com",
        "method": "register",
    },
    "pornhub": {
        "func": pornhub,
        "active": False,
        "description": "pornhub.com",
        "method": "register",
    },
    "protonmail": {
        "func": protonmail,
        "active": True,
        "description": "protonmail.ch",
        "method": "other",
        "client": {
            "request_class": RequestBaseParamsAsync,
            "use_proxy": True,
            "proxy_group": "2",
            "proxy_group_fallback": "2",
        },
    },
    "quora": {
        "func": quora,
        "active": True,
        "description": "quora.com",
        "method": "register",
        "client": {
            "request_class": RequestBaseParamsAsync,
            "use_proxy": True,
            "proxy_group": "2",
            "proxy_group_fallback": "2",
        },
    },
    "rambler": {
        "func": rambler,
        "active": True,
        "description": "rambler.ru",
        "method": "register",
    },
    "redtube": {
        "func": redtube,
        "active": True,
        "description": "redtube.com",
        "method": "register",
        "client": {
            "request_class": RequestBaseParamsAsync,
            "use_proxy": True,
            "proxy_group": "2",
            "proxy_group_fallback": "2",
        },
    },
    "replit": {
        "func": replit,
        "active": True,
        "description": "replit.com",
        "method": "register",
        "client": {"request_class": RequestBaseParamsAsync, "use_proxy": True},
    },
    "rocketreach": {
        "func": rocketreach,
        "active": False,
        "description": "rocketreach.co",
        "method": "register",
    },
    "samsung": {
        "func": samsung,
        "active": False,
        "description": "samsung.com",
        "method": "register",
    },
    "seoclerks": {
        "func": seoclerks,
        "active": True,
        "description": "seoclerks.com",
        "method": "register",
    },
    "sevencups": {
        "func": sevencups,
        "active": True,
        "description": "7cups.com",
        "method": "register",
        "client": {"request_class": RequestBaseParamsAsync, "use_proxy": True},
    },
    "smule": {
        "func": smule,
        "active": False,
        "description": "smule.com",
        "method": "register",
    },
    "snapchat": {
        "func": snapchat,
        "active": False,
        "description": "snapchat.com",
        "method": "login",
    },
    "soundcloud": {
        "func": soundcloud,
        "active": True,
        "description": "soundcloud.com",
        "method": "register",
        "client": {
            "request_class": RequestBaseParamsCFFIAsync,
            "use_proxy": True,
            "proxy_group": "2",
            "proxy_group_fallback": "2",
        },
    },
    "sporcle": {
        "func": sporcle,
        "active": True,
        "description": "sporcle.com",
        "method": "register",
    },
    "spotify": {
        "func": spotify,
        "active": True,
        "description": "spotify.com",
        "method": "register",
    },
    "strava": {
        "func": strava,
        "active": False,
        "description": "strava.com",
        "method": "register",
    },
    "taringa": {
        "func": taringa,
        "active": False,
        "description": "taringa.net",
        "method": "register",
    },
    "teamleader": {
        "func": teamleader,
        "active": False,
        "description": "teamleader.com",
        "method": "register",
    },
    "teamtreehouse": {
        "func": teamtreehouse,
        "active": False,
        "description": "teamtreehouse.com",
        "method": "register",
    },
    "tellonym": {
        "func": tellonym,
        "active": True,
        "description": "tellonym.me",
        "method": "register",
    },
    "thecardboard": {
        "func": thecardboard,
        "active": True,
        "description": "thecardboard.org",
        "method": "register",
    },
    "therianguide": {
        "func": therianguide,
        "active": True,
        "description": "forums.therian-guide.com",
        "method": "register",
    },
    "thevapingforum": {
        "func": thevapingforum,
        "active": False,
        "description": "thevapingforum.com",
        "method": "register",
    },
    "tumblr": {
        "func": tumblr,
        "active": False,
        "description": "tumblr.com",
        "method": "register",
    },
    "tunefind": {
        "func": tunefind,
        "active": False,
        "description": "tunefind.com",
        "method": "register",
    },
    "twitter": {
        "func": twitter,
        "active": True,
        "description": "twitter.com",
        "method": "register",
        "client": {
            "request_class": RequestBaseParamsAsync,
            "use_proxy": True,
            "proxy_group": "2",
            "proxy_group_fallback": "2",
        },
    },
    "venmo": {
        "func": venmo,
        "active": False,
        "description": "venmo.com",
        "method": "register",
    },
    "vivino": {
        "func": vivino,
        "active": False,
        "description": "vivino.com",
        "method": "register",
    },
    "voxmedia": {
        "func": voxmedia,
        "active": True,
        "description": "voxmedia.com",
        "method": "register",
    },
    "vrbo": {
        "func": vrbo,
        "active": True,
        "description": "vrbo.com",
        "method": "register",
        "client": {"request_class": RequestBaseParamsAsync, "use_proxy": True},
    },
    "vsco": {
        "func": vsco,
        "active": False,
        "description": "vsco.co",
        "method": "register",
    },
    "wattpad": {
        "func": wattpad,
        "active": True,
        "description": "wattpad.com",
        "method": "register",
    },
    "wordpress": {
        "func": wordpress,
        "active": True,
        "description": "wordpress",
        "method": "login",
    },
    "xing": {
        "func": xing,
        "active": False,
        "description": "xing.com",
        "method": "register",
    },
    "xnxx": {
        "func": xnxx,
        "active": True,
        "description": "xnxx.com",
        "method": "register",
        "client": {
            "request_class": RequestBaseParamsAsync,
            "use_proxy": True,
            "proxy_group": "2",
            "proxy_group_fallback": "2",
        },
    },
    "xvideos": {
        "func": xvideos,
        "active": True,
        "description": "xvideos.com",
        "method": "register",
        "client": {
            "request_class": RequestBaseParamsAsync,
            "use_proxy": True,
            "proxy_group": "2",
            "proxy_group_fallback": "2",
        },
    },
    "yahoo": {
        "func": yahoo,
        "active": False,
        "description": "yahoo.com",
        "method": "login",
    },
    "zoho": {
        "func": zoho,
        "active": False,
        "description": "zoho.com",
        "method": "login",
    },
}


MODULES = list(module_mapping.keys())
ACTIVE_MODULES = [key for key in MODULES if get(module_mapping, f"{key}.active")]
