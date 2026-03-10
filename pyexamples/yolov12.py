import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from pycore.tikzeng import *


arch = [
    to_head(".."),
    to_cor(),
    to_begin(),

    # Input
    to_input("../examples/fcn8s/cats.jpg", to="(-5,0,0)", width=5, height=5, name="input"),

    # Backbone
    to_Conv("conv1", 64, 320, offset="(0,0,0)", to="(0,0,0)", width=1.8, height=30, depth=30, caption="Conv"),
    to_Conv("conv2", 128, 160, offset="(2.3,0,0)", to="(conv1-east)", width=2.0, height=26, depth=26, caption="Conv"),
    to_connection("conv1", "conv2"),

    to_Conv("c3k2_p2", 256, 160, offset="(2.4,0,0)", to="(conv2-east)", width=2.4, height=26, depth=26, caption="C3k2 x2"),
    to_connection("conv2", "c3k2_p2"),

    to_Conv("conv_p3", 256, 80, offset="(2.4,0,0)", to="(c3k2_p2-east)", width=2.2, height=22, depth=22, caption="Conv s2"),
    to_connection("c3k2_p2", "conv_p3"),

    to_Conv("c3k2_p3", 512, 80, offset="(2.4,0,0)", to="(conv_p3-east)", width=2.8, height=22, depth=22, caption="C3k2 x2"),
    to_connection("conv_p3", "c3k2_p3"),

    to_Conv("conv_p4", 512, 40, offset="(2.4,0,0)", to="(c3k2_p3-east)", width=2.5, height=17, depth=17, caption="Conv s2"),
    to_connection("c3k2_p3", "conv_p4"),

    to_Conv("a2c2f_p4", 512, 40, offset="(2.4,0,0)", to="(conv_p4-east)", width=3.1, height=17, depth=17, caption="A2C2f x4"),
    to_connection("conv_p4", "a2c2f_p4"),

    to_Conv("conv_p5", 1024, 20, offset="(2.4,0,0)", to="(a2c2f_p4-east)", width=2.8, height=13, depth=13, caption="Conv s2"),
    to_connection("a2c2f_p4", "conv_p5"),

    to_Conv("a2c2f_p5", 1024, 20, offset="(2.4,0,0)", to="(conv_p5-east)", width=3.2, height=13, depth=13, caption="A2C2f x4"),
    to_connection("conv_p5", "a2c2f_p5"),

    # Neck: top-down path
    to_Conv("up_p5", 1024, 40, offset="(3.2,4.8,0)", to="(a2c2f_p5-east)", width=2.8, height=17, depth=17, caption="Upsample x2"),
    to_connection("a2c2f_p5", "up_p5"),

    to_Conv("concat_p4", 1536, 40, offset="(2.0,0,0)", to="(up_p5-east)", width=2.1, height=17, depth=17, caption="Concat"),
    to_connection("up_p5", "concat_p4"),
    to_skip("a2c2f_p4", "concat_p4", pos=1.25),

    to_Conv("fuse_p4", 512, 40, offset="(2.0,0,0)", to="(concat_p4-east)", width=3.0, height=17, depth=17, caption="A2C2f x2"),
    to_connection("concat_p4", "fuse_p4"),

    to_Conv("up_p4", 512, 80, offset="(3.0,4.2,0)", to="(fuse_p4-east)", width=2.5, height=22, depth=22, caption="Upsample x2"),
    to_connection("fuse_p4", "up_p4"),

    to_Conv("concat_p3", 1024, 80, offset="(2.0,0,0)", to="(up_p4-east)", width=2.1, height=22, depth=22, caption="Concat"),
    to_connection("up_p4", "concat_p3"),
    to_skip("c3k2_p3", "concat_p3", pos=1.25),

    to_Conv("fuse_p3", 256, 80, offset="(2.0,0,0)", to="(concat_p3-east)", width=2.8, height=22, depth=22, caption="A2C2f x2"),
    to_connection("concat_p3", "fuse_p3"),

    to_Conv("det_p3", 256, 80, offset="(2.3,4.0,0)", to="(fuse_p3-east)", width=2.2, height=22, depth=22, caption="Detect P3"),
    to_connection("fuse_p3", "det_p3"),

    # Head: bottom-up path
    to_Conv("down_p3", 256, 40, offset="(3.0,-4.4,0)", to="(fuse_p3-east)", width=2.3, height=17, depth=17, caption="Conv s2"),
    to_connection("fuse_p3", "down_p3"),

    to_Conv("concat_h4", 768, 40, offset="(2.0,0,0)", to="(down_p3-east)", width=2.1, height=17, depth=17, caption="Concat"),
    to_connection("down_p3", "concat_h4"),
    to_skip("fuse_p4", "concat_h4", pos=1.25),

    to_Conv("head_p4", 512, 40, offset="(2.0,0,0)", to="(concat_h4-east)", width=2.9, height=17, depth=17, caption="A2C2f x2"),
    to_connection("concat_h4", "head_p4"),

    to_Conv("det_p4", 512, 40, offset="(2.3,-3.8,0)", to="(head_p4-east)", width=2.3, height=17, depth=17, caption="Detect P4"),
    to_connection("head_p4", "det_p4"),

    to_Conv("down_p4", 512, 20, offset="(3.0,-4.4,0)", to="(head_p4-east)", width=2.5, height=13, depth=13, caption="Conv s2"),
    to_connection("head_p4", "down_p4"),

    to_Conv("concat_h5", 1536, 20, offset="(2.0,0,0)", to="(down_p4-east)", width=2.1, height=13, depth=13, caption="Concat"),
    to_connection("down_p4", "concat_h5"),
    to_skip("a2c2f_p5", "concat_h5", pos=1.25),

    to_Conv("head_p5", 1024, 20, offset="(2.0,0,0)", to="(concat_h5-east)", width=3.0, height=13, depth=13, caption="C3k2 x2"),
    to_connection("concat_h5", "head_p5"),

    to_Conv("det_p5", 1024, 20, offset="(2.3,-3.8,0)", to="(head_p5-east)", width=2.5, height=13, depth=13, caption="Detect P5"),
    to_connection("head_p5", "det_p5"),

    to_end(),
]


def main():
    namefile = str(sys.argv[0]).split(".")[0]
    to_generate(arch, namefile + ".tex")


if __name__ == "__main__":
    main()
