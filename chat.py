#!/usr/bin/env python3
import argparse

from dotenv import load_dotenv

from localchat.client import DEFAULT_MODEL
from localchat.session import run

load_dotenv()

p = argparse.ArgumentParser()
p.add_argument("--model", default=DEFAULT_MODEL)
p.add_argument("--temperature", type=float, default=0.6)
args = p.parse_args()

run(model=args.model, temperature=args.temperature)
