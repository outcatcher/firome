import argparse
import logging
import time

from firome.logging import LOGGER
from firome.merge import merge
from firome.export.tcx import export_as_tcx

parser = argparse.ArgumentParser(
    description="Combines GPX file with training data with GPX file with position data based on the distance"
)
parser.add_argument("--route", type=str, required=True, help="Path to GPX file with route of the training")
parser.add_argument("--recording", type=str, required=True, help="Path to FIT file with GPS-less data of the training")
parser.add_argument("--precision", type=float, default=1.0, help="Precision of interpolation, meters")
parser.add_argument("--output", choices=["tcx"], default="tcx", help="Output format")
parser.add_argument("--debug", action="store_true", help="Enable debug logging")

if __name__ == "__main__":
    args = parser.parse_args()

    LOGGER.info("route: %s", args.route)
    LOGGER.info("recording: %s", args.recording)

    if args.debug:
        LOGGER.setLevel(logging.DEBUG)

    points = merge(args.route, args.recording, args.precision)

    if args.output == "tcx":
        output_path = f"{int(time.time())}.tcx"

        export_as_tcx(points, output_path)

        LOGGER.info("\nresult: %s", output_path)
