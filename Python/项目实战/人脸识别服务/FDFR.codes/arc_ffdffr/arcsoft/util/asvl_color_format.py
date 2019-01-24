#! -*- coding: utf-8 -*-


# author: forcemain@163.com


# R  R  R  R  R  G  G  G  G  G  G  B  B  B  B  B
ASVL_PAF_RGB16_B5G6R5 = 0x101
# X  R  R  R  R  R  G  G  G  G  G  B  B  B  B  B
ASVL_PAF_RGB16_B5G5R5 = 0x102
# X  X  X  X  R  R  R  R  G  G  G  G  B  B  B  B
ASVL_PAF_RGB16_B4G4R4 = 0x103
# T  R  R  R  R  R  G  G  G  G  G  B  B  B  B  B
ASVL_PAF_RGB16_B5G5R5T = 0x104
# B  B  B  B  B  G  G  G  G  G  G  R  R  R  R  R
ASVL_PAF_RGB16_R5G6B5 = 0x105
# X  B  B  B  B  B  G  G  G  G  G  R  R  R  R  R
ASVL_PAF_RGB16_R5G5B5 = 0x106
# X  X  X  X  B  B  B  B  G  G  G  G  R  R  R  R
ASVL_PAF_RGB16_R4G4B4 = 0x107

# R	R  R  R	 R	R  R  R  G  G  G  G  G  G  G  G  B  B  B  B  B  B  B  B
ASVL_PAF_RGB24_B8G8R8 = 0x201
# X	X  X  X	 X	X  R  R  R  R  R  R  G  G  G  G  G  G  B  B  B  B  B  B
ASVL_PAF_RGB24_B6G6R6 = 0x202
# X	X  X  X	 X	T  R  R  R  R  R  R  G  G  G  G  G  G  B  B  B  B  B  B
ASVL_PAF_RGB24_B6G6R6T = 0x203
# B  B  B  B  B  B  B  B  G  G  G  G  G  G  G  G  R	R  R  R	 R	R  R  R
ASVL_PAF_RGB24_R8G8B8 = 0x204
# X	X  X  X	 X	X  B  B  B  B  B  B  G  G  G  G  G  G  R  R  R  R  R  R
ASVL_PAF_RGB24_R6G6B6 = 0x205

# X	X  X  X	 X	X  X  X	 R	R  R  R	 R	R  R  R  G  G  G  G  G  G  G  G  B  B  B  B  B  B  B  B
ASVL_PAF_RGB32_B8G8R8 = 0x301
# A	A  A  A	 A	A  A  A	 R	R  R  R	 R	R  R  R  G  G  G  G  G  G  G  G  B  B  B  B  B  B  B  B
ASVL_PAF_RGB32_B8G8R8A8 = 0x302
# X	X  X  X	 X	X  X  X	 B  B  B  B  B  B  B  B  G  G  G  G  G  G  G  G  R	R  R  R	 R	R  R  R
ASVL_PAF_RGB32_R8G8B8 = 0x303
# B    B  B  B  B  B  B  B  G  G  G  G  G  G  G  G  R  R  R  R  R  R  R  R  A	A  A  A  A	A  A  A
ASVL_PAF_RGB32_A8R8G8B8 = 0x304
# A    A  A  A  A  A  A  A  B  B  B  B  B  B  B  B  G  G  G  G  G  G  G  G  R  R  R  R  R	R  R  R
ASVL_PAF_RGB32_R8G8B8A8 = 0x305

# Y0, U0, V0
ASVL_PAF_YUV = 0x401
# Y0, V0, U0
ASVL_PAF_YVU0 = 0x402
# U0, V0, Y0
ASVL_PAF_UVY = 0x403
# V0, U0, Y0
ASVL_PAF_VUY = 0x404

# Y0, U0, Y1, V0
ASVL_PAF_YUYV = 0x501
# Y0, V0, Y1, U0
ASVL_PAF_YVYU = 0x502
# U0, Y0, V0, Y1
ASVL_PAF_UYVY = 0x503
# V0, Y0, U0, Y1
ASVL_PAF_VYUY = 0x504
# Y1, U0, Y0, V0
ASVL_PAF_YUYV2 = 0x505
# Y1, V0, Y0, U0
ASVL_PAF_YVYU2 = 0x506
# U0, Y1, V0, Y0
ASVL_PAF_UYVY2 = 0x507
# V0, Y1, U0, Y0
ASVL_PAF_VYUY2 = 0x508
# Y0, Y1, U0, V0
ASVL_PAF_YYUV = 0x509

# I420(IYUV)
# 8-bit Y层，之后是8-bit的2x2 采样的U层和V层
ASVL_PAF_I420 = 0x601
# 8 bit Y plane followed by 8 bit 1x2 subsampled U and V planes
ASVL_PAF_I422V = 0x602
# 8 bit Y plane followed by 8 bit 2x1 subsampled U and V planes
ASVL_PAF_I422H = 0x603
# 8 bit Y plane followed by 8 bit U and V planes
ASVL_PAF_I444 = 0x604
# 8 bit Y plane followed by 8 bit 2x2 subsampled V and U planes
ASVL_PAF_YV12 = 0x605
# 8 bit Y plane followed by 8 bit 1x2 subsampled V and U planes
ASVL_PAF_YV16V = 0x606
# 8 bit Y plane followed by 8 bit 2x1 subsampled V and U planes
ASVL_PAF_YV16H = 0x607
# 8 bit Y plane followed by 8 bit V and U planes
ASVL_PAF_YV24 = 0x608

# 8 bit Y plane only
ASVL_PAF_GRAY = 0x701

# 8 bit Y plane followed by 8 bit 2x2 subsampled UV planes
ASVL_PAF_NV12 = 0x801
# 8 bit Y plane followed by 8 bit 2x2 subsampled VU planes
ASVL_PAF_NV21 = 0x802
# 8 bit Y plane followed by 8 bit 2x1 subsampled UV planes
ASVL_PAF_LPI422H = 0x803
# 8 bit Y plane followed by 8 bit 2x1 subsampled VU planes
ASVL_PAF_LPI422H2 = 0x804
# 8 bit Y plane followed by 8 bit 4x4 subsampled VU planes
ASVL_PAF_NV41 = 0x805

ASVL_PAF_RAW10_RGGB_10B = 0xd01
ASVL_PAF_RAW10_GRBG_10B = 0xd02
ASVL_PAF_RAW10_GBRG_10B = 0xd03
ASVL_PAF_RAW10_BGGR_10B = 0xd04

ASVL_PAF_RAW12_RGGB_12B = 0xd05
ASVL_PAF_RAW12_GRBG_12B = 0xd06
ASVL_PAF_RAW12_GBRG_12B = 0xd07
ASVL_PAF_RAW12_BGGR_12B = 0xd08

ASVL_PAF_RAW10_RGGB_16B = 0xd09
ASVL_PAF_RAW10_GRBG_16B = 0xd0A
ASVL_PAF_RAW10_GBRG_16B = 0xd0B
ASVL_PAF_RAW10_BGGR_16B = 0xd0C

# 10 bits gray raw data
ASVL_PAF_RAW10_GRAY_10B = 0xe01

# 10 bits gray raw data, each data has 2 bytes
ASVL_PAF_RAW10_GRAY_16B = 0xe81
