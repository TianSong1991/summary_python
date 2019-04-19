#include <stdio.h>
#include "iostream"
#include <fstream>
#include <opencv2/opencv.hpp>
#include <string>

using namespace std;
using namespace cv;

int main()
{
	cv::FileStorage fs;
	for (int i = 0; i < 59; i++) {
		cv::Mat imgdepth,imgrgb,imgmap;
		cv::FileStorage fs("F:\\adb\\depth"+ std::to_string(i) +".yml", cv::FileStorage::READ);
		fs["depth"] >> imgdepth;
		imgdepth = imgdepth * 50;
		cv::FileStorage fs1("F:\\adb\\rbg" + std::to_string(i) + ".yml", cv::FileStorage::READ);
		fs1["rgb"] >> imgrgb;
		cv::FileStorage fs2("F:\\adb\\map" + std::to_string(i) + ".yml", cv::FileStorage::READ);
		fs2["map"] >> imgmap;
		cout << "picture:"  << i << endl << endl;
	}

	fs.release();
	system("pause");
	return 0;
}