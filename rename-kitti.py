import os
import argparse
import cv2
import glob
import shutil

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Lama data tool')
    parser.add_argument('--mask_root', type=str)
    parser.add_argument('--img_root', type=str) # D:\MyProject\PyThon\FlowInpainting\lama\KITTI360-EX\OuterPinhole\imgs\
    parser.add_argument('--result_root', type=str)
    parser.add_argument('--resize_root', type=str)
    args = parser.parse_args()

    if args.mask_root is not None:
        # 给所有mask图片加上后缀，并移动到根目录重新排序
        # 读取视频list
        video_list = []
        for root, dirs, files in os.walk(args.mask_root, topdown=False):
            # 获取文件夹名字
            video_list = dirs

        # mask的工作循环
        mask_index = 0  # 重新命名mask的index
        for v in range(len(video_list)):

            # 取出一个video地址
            video = video_list[v]

            # frame_dir直接用根目录+视频名字就可以了
            frame_dir = os.path.join(args.mask_root, video)

            # 我们的图像是png格式
            frame_list = glob.glob(os.path.join(frame_dir, "*.png"))

            video_length = len(frame_list)
            # 当前视频的工作循环
            for t in range(0, len(frame_list)):
                video_name = video.split('//')[-1]

                # 重命名mask
                # mask是png格式的哦
                filename = os.path.join(frame_dir, "%06d.png" % t)
                new_filename = os.path.join(frame_dir, "%08d_mask.png" % mask_index)
                os.rename(filename, new_filename)

                # 移动mask到上一级目录
                dst = os.path.join(args.mask_root, "%08d_mask.png" % mask_index)
                mask_index += 1
                shutil.move(new_filename, dst)

    if args.img_root is not None:
        # 把各个小文件夹的图片挪到根目录并且重新命名
        # 读取视频list
        video_list = []
        for root, dirs, files in os.walk(args.img_root, topdown=False):
            # 获取文件夹名字
            video_list = dirs

        # img的工作循环
        img_index = 0  # 重新命名img的index
        for v in range(len(video_list)):

            # 取出一个video地址
            video = video_list[v]

            # frame_dir直接用根目录+视频名字就可以了
            frame_dir = os.path.join(args.img_root, video)

            # 我们的图像是jpg格式
            frame_list = glob.glob(os.path.join(frame_dir, "*.jpg"))

            video_length = len(frame_list)
            # 当前视频的工作循环
            for t in range(0, len(frame_list)):
                video_name = video.split('//')[-1]

                # 重命名img
                # img是jpg格式的哦
                filename = os.path.join(frame_dir, "%06d.jpg" % t)
                new_filename = os.path.join(frame_dir, "%08d.jpg" % img_index)
                os.rename(filename, new_filename)

                # 移动img到上一级目录
                dst = os.path.join(args.img_root, "%08d.jpg" % img_index)
                img_index += 1
                shutil.move(new_filename, dst)

    if args.result_root is not None:
        # 把根目录的图片挪到各个小文件夹并且重新命名
        # 读取图片的list
        frame_dir = args.result_root
        frame_list = glob.glob(os.path.join(frame_dir, "*.png"))
        # frame_list = glob.glob(os.path.join(frame_dir, "*.jpg"))

        # 生成视频list
        video_list = []
        for v in range(719, 757):
            # 获取文件夹名字
            video_dir = os.path.join(args.result_root, str(v).zfill(8))
            video_list.append(video_dir)
            if not os.path.exists(video_dir):
                os.mkdir(video_dir)

        # img的工作循环
        img_index = 0       # 每个子目录下img的名字
        video_index = 0     # 子目录的名字index
        for t in range(0, len(frame_list)):
            # 重命名img
            # img是png格式的哦
            # filename = os.path.join(frame_dir, "%08d_mask.png" % t)
            # new_filename = os.path.join(frame_dir, "%08d.png" % img_index)
            # os.rename(filename, new_filename)

            # 不重命名
            # filename = os.path.join(frame_dir, "%08d.jpg" % t)
            filename = os.path.join(frame_dir, "%08d.png" % t)

            # 移动img到新建的子目录
            # dst = os.path.join(video_list[video_index], "%08d.png" % img_index)
            # print(dst)
            # shutil.move(new_filename, dst)

            # 不重命名
            # dst = os.path.join(video_list[video_index], "%08d.jpg" % img_index)
            dst = os.path.join(video_list[video_index], "%08d.png" % img_index)
            print(dst)
            shutil.move(filename, dst)

            if img_index == 99:
                # 下一个视频
                img_index = 0
                video_index += 1
            else:
                img_index += 1

    if args.resize_root is not None:
        # 用于把目录下所有的图片resize
        # 读取图片的list
        frame_dir = args.resize_root
        frame_list = glob.glob(os.path.join(frame_dir, "*.png"))
        # frame_list = glob.glob(os.path.join(frame_dir, "*.jpg"))

        for t in range(0, len(frame_list)):
            # 当前图片的名字
            # filename = os.path.join(frame_dir, "%08d.png" % t)
            filename = os.path.join(frame_dir, "%08d_mask.png" % t)
            # filename = os.path.join(frame_dir, "%08d.jpg" % t)

            # resize
            img = cv2.imread(filename)
            img = cv2.resize(img, (256, 256))   # w h
            print(filename)

            # save 注意会覆盖
            cv2.imwrite(filename, img)
