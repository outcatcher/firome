import argparse
import logging
import sys
import time

from firome import __version__
from firome.codecs.tcx import export_as_tcx
from firome.logger import LOGGER
from firome.merge import merge


def __no_prio_args():
    return "--version" not in sys.argv


parser = argparse.ArgumentParser(
    description="Combines GPX file with training data with GPX file with position data based on the distance",
)
parser.add_argument("--route", type=str, required=__no_prio_args(),
                    help="Path to GPX file with route of the training")
parser.add_argument("--recording", type=str, required=__no_prio_args(),
                    help="Path to FIT file with GPS-less data of the training")
parser.add_argument("--precision", type=float, default=1.0, help="Precision of interpolation, meters")
parser.add_argument("--output", choices=["tcx"], default="tcx", help="Output format")
parser.add_argument("--debug", action="store_true", help="Enable debug logging")
parser.add_argument("--version", action="store_true", help="Print app version")

if __name__ == "__main__":
    args = parser.parse_args()

    if args.version:
        print(__version__)  # noqa: T201  # not for debug
        sys.exit(0)

    LOGGER.info("route: %s", args.route)
    LOGGER.info("recording: %s", args.recording)

    if args.debug:
        LOGGER.setLevel(logging.DEBUG)

    points = merge(args.route, args.recording, args.precision)

    if args.output == "tcx":
        output_path = f"{int(time.time())}.tcx"

        export_as_tcx(points, output_path)

        LOGGER.info("\nresult: %s", output_path)
