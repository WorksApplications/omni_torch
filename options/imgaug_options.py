import argparse


class ImgAug:
    def initialize(self):
        self.parser = argparse.ArgumentParser()
        # Todo: the role of random_crop and crop_size is still unclear
        self.parser.add_argument("--random_crop", type=bool, default=True,
                                 help="randomly crop an image")
        self.parser.add_argument("--crop_size", type=tuple, default=(512, 512),
                                 help="size of input images")

        self.parser.add_argument("--segments", type=tuple,
                                 help="sliced in W and H dimension of an image")
        self.parser.add_argument("--patch_size", type=tuple, default=(320, 320),
                                 help="the size of segmented patches from origin image")

        self.parser.add_argument("--img_size", type=tuple, default=(320, 320),
                                 help="size of input images")
        self.parser.add_argument("--img_channel", type=int, default=3,
                                 help="3 stand for color image while 1 for greyscale")

        self.parser.add_argument("--perform_ops", type=bool, default=True,
                                 help="inverse the image bitwise")
        self.parser.add_argument("--do_imgaug", type=bool, default=True,
                                 help="do image augmentation on image or not")

        self.parser.add_argument("--random_flip", type=bool, default=True,
                                 help="randomly flip an image")
        self.parser.add_argument("--aug_bg_color", type=int, default=255,
                                 help="background color of augmentation")
        self.parser.add_argument("--random_brightness", type=bool, default=False,
                                 help="adjust brightness on image")
        self.parser.add_argument("--random_noise", type=bool, default=False,
                                 help="apply random gaussian noise on image")
        
        self.parser.add_argument("--translation", type=tuple, default=(0.00, 0.00),
                                 help="a list of two elements indicate translation on x and y axis")
        self.parser.add_argument("--scale", type=tuple, default=(1, 1),
                                 help="a list of two elements indicate scale on x and y axis")
        self.parser.add_argument("--shear", type=tuple, default=(0, 0),
                                 help="a list of two elements indicate shear on x and y axis")
        self.parser.add_argument("--rotation", type=tuple, default=(0, 0),
                                 help="a number indicate rotation of image")

        
        self.parser.add_argument("--imgaug_max_delta", type=float, default=0.2,
                                 help="random up bound of brightness adjustment")
        self.parser.add_argument("--imgaug_mean", type=float, default=0.0,
                                 help="mean of random coefficiency of translation")
        self.parser.add_argument("--imgaug_stddev", type=float, default=0.2,
                                 help="standard deviation of random coefficiency of translation")
        self.parser.add_argument("--imgaug_crop_bbox", type=bool, default=False,
                                 help="crop the bound box from image or not")
