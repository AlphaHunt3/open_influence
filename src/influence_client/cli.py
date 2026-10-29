"""MCP by default; explicit JSON commands for terminals and agent Skills."""
import argparse
import asyncio
import json
import sys

from .client import InfluenceClient, InfluenceError
from . import __version__


def parser():
    p = argparse.ArgumentParser(description="XHunt influence intelligence: MCP server, CLI and Python client")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="command")
    sub.add_parser("serve", help="Run the stdio MCP server (default)")
    sub.add_parser("capabilities", help="Public coverage metadata; zero credits, no key")
    sub.add_parser("usage", help="Your current credit balance; zero credits")
    x = sub.add_parser("x", help="X influence or rank-gain leaderboard")
    x.add_argument("--kind", choices=["influence", "weekly_growth"], default="influence")
    x.add_argument("--sector", choices=["ai", "web3"], default="web3")
    x.add_argument("--region", choices=["global", "en", "cn"], default="global")
    x.add_argument("--limit", type=int, default=10)
    profile = sub.add_parser("profile", help="One X profile; one credit")
    profile.add_argument("handle")
    for name, help_text in (
        ("ranks", "Six X sector/region ranks and available source population counts; one credit"),
        ("profile-history", "Recorded X profile snapshots; one credit per handle"),
    ):
        command = sub.add_parser(name, help=help_text)
        command.add_argument("handle")
    followers = sub.add_parser("smart-followers", help="X global/cn Top10 followers; up to20 credits")
    followers.add_argument("handle")
    followers.add_argument("--sector", choices=["ai", "web3"], default="web3")
    social = sub.add_parser("social", help="Monitored X events; limit per type, up to4*limit credits")
    social.add_argument("handle")
    social.add_argument("--limit", type=int, default=10)
    circle = sub.add_parser("circle", help="Observed bilateral direct interaction Top10; up to10 credits")
    circle.add_argument("handle")
    circle.add_argument("--days", type=int, default=7)
    abilities = sub.add_parser("abilities", help="Published X abilities >=85; one credit")
    abilities.add_argument("handle")
    abilities.add_argument("--sector", choices=["ai", "web3"], default="web3")
    weekly = sub.add_parser("weekly", help="X attention or Top200 entries versus baseline")
    weekly.add_argument("--mode", choices=["attention", "new_entries"], default="attention")
    weekly.add_argument("--sector", choices=["ai", "web3"], default="web3")
    weekly.add_argument("--region", choices=["global", "en", "cn"], default="cn")
    weekly.add_argument("--limit", type=int, default=10)
    square = sub.add_parser("square", help="Square influence leaderboard")
    square.add_argument("--limit", type=int, default=10)
    for name in ("square-profile", "square-abilities"):
        command = sub.add_parser(name)
        command.add_argument("square_uid")
    sw = sub.add_parser("square-weekly", help="Square 7-day absolute net follower gain")
    sw.add_argument("--metric", choices=["followers", "smart_followers"], default="followers")
    sw.add_argument("--limit", type=int, default=10)
    sw.add_argument("--region", choices=["global", "en", "cn"], default="global")
    yt = sub.add_parser("youtube", help="Weekly YouTube AI/Web3 leaderboard")
    yt.add_argument("--sector", choices=["ai", "web3"], default="web3")
    yt.add_argument("--limit", type=int, default=10)
    return p


async def run(args):
    methods = {"capabilities": "capabilities", "usage": "usage", "x": "x_leaderboard", "profile": "x_profile",
               "ranks": "x_ranks", "smart-followers": "x_smart_followers",
               "circle": "x_circle", "social": "x_social", "profile-history": "x_profile_history",
               "abilities": "x_abilities", "weekly": "x_weekly", "square": "square_leaderboard",
               "square-profile": "square_profile", "square-abilities": "square_abilities",
               "square-weekly": "square_weekly", "youtube": "youtube_leaderboard"}
    kwargs = {k: v for k, v in vars(args).items() if k != "command"}
    async with InfluenceClient() as client:
        return await getattr(client, methods[args.command])(**kwargs)


def main():
    args = parser().parse_args()
    if args.command in (None, "serve"):
        from .server import main as serve
        serve()
        return
    try:
        result = asyncio.run(run(args))
    except InfluenceError as exc:
        print(json.dumps(exc.as_dict(), ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1)
    except KeyboardInterrupt:
        raise SystemExit(130)
    print(json.dumps(result, ensure_ascii=False, indent=2))
