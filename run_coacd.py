# Based on https://github.com/SarahWeiii/CoACD/blob/main/python/package/bin/coacd only difference is that this script will output each part as a separate file

import trimesh
import numpy as np
import sys
import os
import argparse
import coacd
import pathlib

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        help="input model loaded by trimesh. Supported formats: glb, gltf, obj, off, ply, stl, etc.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="output model exported by trimesh. Supported formats: glb, gltf, obj, off, ply, stl, etc.",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        type=float,
        default=0.05,
        help="termination criteria in [0.01, 1] (0.01: most fine-grained; 1: most coarse)",
    )

    args = parser.parse_args()

    input_file = pathlib.Path(args.input)
    output_file = pathlib.Path(args.output)

    if not os.path.isfile(input_file):
        print(input_file, "is not a file")
        exit(1)

    mesh = trimesh.load(input_file, force="mesh")
    mesh = coacd.Mesh(mesh.vertices, mesh.faces)
    result = coacd.run_coacd(
        mesh,
        threshold=args.threshold,
    )
    mesh_parts = []
    for vs, fs in result:
        mesh_parts.append(trimesh.Trimesh(vs, fs))
    np.random.seed(0)
    for idx, p in enumerate(mesh_parts):
        scene = trimesh.Scene()
        p.visual.vertex_colors[:, :3] = (np.random.rand(3) * 255).astype(np.uint8)
        scene.add_geometry(p)
        output_file.mkdir(parents=True, exist_ok=True)
        scene.export(output_file / f"{idx}{input_file.suffix}")
