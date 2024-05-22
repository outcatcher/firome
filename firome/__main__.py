import argparse
import time

from firome.merge import merge
from firome.export.tcx import export_as_tcx

parser = argparse.ArgumentParser(
    description="Combines GPX file with training data with GPX file with position data based on the distance")
parser.add_argument("--route", type=str, required=True, help="Path to GPX file with route of the training")
parser.add_argument("--recording", type=str, required=True, help="Path to FIT file with GPS-less data of the training")
parser.add_argument("--output", choices=["tcx"], default="tcx", help="Output format")

if __name__ == '__main__':
    args = parser.parse_args()

    print("route: ", args.route)
    print("recording: ", args.recording)

    points = merge(args.route, args.recording)

    if args.output == "tcx":
        output_path = f"{int(time.time())}.tcx"

        export_as_tcx(points, output_path)

        print()
        print("result: ", output_path)
