-- SQLite
/*
 Navicat Premium Data Transfer

 Source Server         : db
 Source Server Type    : SQLite
 Source Server Version : 3030001
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3030001
 File Encoding         : 65001

 Date: 18/07/2023 00:01:51
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for Users
-- ----------------------------
DROP TABLE IF EXISTS "Users";
CREATE TABLE "Users" (
  "id" integer(32) NOT NULL,
  "username" text(64),
  "email" text(64),
  "password" blob,
  "oauth_github" text(100),
  CONSTRAINT "Users_pkey" PRIMARY KEY ("id")
);

-- ----------------------------
-- Records of Users
-- ----------------------------
INSERT INTO "Users" VALUES (1, 'kasper andersson', 'skyeagle0907@gmail.com', 'b2a248e1f1b3f4115b4f94d265f4e8899bf5b07b61649d5977445318d365c00c0fd711d17f1a740bddb7f44ef58e570b718a4ea5ff8c1ceba6b0eaff3bd37e999e797b850ca36396f56bd648bb44e23afd784c2eb598dca6e092e7de9f3f1800', NULL);
INSERT INTO "Users" VALUES (2, 'michaelbage', 'michael.bage@hotmail.se', 'a96dfd528ca61700a6ca6a89f10f2b474663a5dfcf63a2f32168ac892d121b6626c67f9db5e9f3942886f06c8528da22e2310102c3776c40cf1fdd5393822185cf073f6b6c09294cf58b52f0aa685f76de3c9483a8e30fcd80eae83299bc25d4', NULL);
INSERT INTO "Users" VALUES (3, 1, '1@1.com', 'd2501f1a886a7dad3b4a7f1cebad4af8391f1086be1c53591058cf5550f0e8714c640066110300fbd548892e93ebacdf2e6b2ad46d7981d5233c59ccf5eda331e19c2b1f53a4d779de23d5157ca3916338dacae842428d88993da499023389ad', NULL);

-- ----------------------------
-- Table structure for tb_birthpattern
-- ----------------------------
DROP TABLE IF EXISTS "tb_birthpattern";
CREATE TABLE "tb_birthpattern" (
  "id" integer(32) NOT NULL,
  "pattern" text,
  "description" text,
  CONSTRAINT "tb_birthpattern_pkey" PRIMARY KEY ("id")
);

-- ----------------------------
-- Records of tb_birthpattern
-- ----------------------------
INSERT INTO "tb_birthpattern" VALUES (1, 'YYYYMMDD', NULL);
INSERT INTO "tb_birthpattern" VALUES (2, 'YYYY', NULL);
INSERT INTO "tb_birthpattern" VALUES (3, 'MMDD', NULL);
INSERT INTO "tb_birthpattern" VALUES (4, 'MM', NULL);
INSERT INTO "tb_birthpattern" VALUES (7, 'Y0M0', NULL);
INSERT INTO "tb_birthpattern" VALUES (8, 'M0D0', NULL);

-- ----------------------------
-- Table structure for tb_patterns
-- ----------------------------
DROP TABLE IF EXISTS "tb_patterns";
CREATE TABLE "tb_patterns" (
  "id" integer(32),
  "type" integer(32),
  "pattern" text,
  "rank" real(53),
  "description" text
);

-- ----------------------------
-- Records of tb_patterns
-- ----------------------------
INSERT INTO "tb_patterns" VALUES (3, 2, 'FNSN', 1.0, 'First Name + Second Name');
INSERT INTO "tb_patterns" VALUES (4, 2, 'SNFN', 1.0, 'Second Name + First Name');
INSERT INTO "tb_patterns" VALUES (5, 2, 'FN.SN', 2.0, 'First Name + dot + Second Name');
INSERT INTO "tb_patterns" VALUES (6, 2, 'FN_SN', 2.0, 'First Name + underscore + Second Name');
INSERT INTO "tb_patterns" VALUES (7, 2, 'SN.FN', 2.0, 'Second Name + dot + First Name');
INSERT INTO "tb_patterns" VALUES (8, 2, 'SN_FN', 2.0, 'Second Name + underscore + First Name');
INSERT INTO "tb_patterns" VALUES (9, 2, 'FTN.SN', 3.0, 'First Name Initial + dot + Second Name');
INSERT INTO "tb_patterns" VALUES (10, 2, 'FN.STN', 3.0, 'First Name + dot + Second Name Initial');
INSERT INTO "tb_patterns" VALUES (11, 2, 'FTN_SN', 4.0, 'First Name Initial + underscore + Second Name');
INSERT INTO "tb_patterns" VALUES (12, 2, 'FN_STN', 4.0, 'First Name + underscore + Second Name Initial');
INSERT INTO "tb_patterns" VALUES (13, 2, 'STN.FN', 5.0, 'Second Name Initial + dot + First Name');
INSERT INTO "tb_patterns" VALUES (14, 2, 'SN.FTN', 5.0, 'Second Name + dot + First Name Initial');
INSERT INTO "tb_patterns" VALUES (15, 2, 'STN_FN', 6.0, 'Second Name Initial + underscore + First Name');
INSERT INTO "tb_patterns" VALUES (16, 2, 'SN_FTN', 6.0, 'Second Name + underscore + First Name Initial');
INSERT INTO "tb_patterns" VALUES (17, 2, 'FTX.SN', 7.0, 'First Name Letters + dot + Second Name');
INSERT INTO "tb_patterns" VALUES (18, 2, 'FTX_SN', 7.0, 'First Name Letters + underscore + Second Name');
INSERT INTO "tb_patterns" VALUES (20, 2, 'FN_STX', 7.0, 'First Name + underscore + Second Name Letters');
INSERT INTO "tb_patterns" VALUES (22, 2, 'STX_FN', 8.0, 'Second Name Letters + underscore + First Name');
INSERT INTO "tb_patterns" VALUES (24, 2, 'SN_FTX', 8.0, 'Second Name + underscore + First Name Letters');
INSERT INTO "tb_patterns" VALUES (25, 3, 'FN', 1.0, 'First Name');
INSERT INTO "tb_patterns" VALUES (27, 3, 'MN', 1.0, 'Middle Name');
INSERT INTO "tb_patterns" VALUES (28, 3, 'FNSN', 2.0, 'First Name + Second Name');
INSERT INTO "tb_patterns" VALUES (30, 3, 'MNFN', 2.0, 'Middle Name + First Name');
INSERT INTO "tb_patterns" VALUES (76, 3, 'FNSN.MTN', 10.0, 'First Name + Second Name + dot + Middle Name Initial');
INSERT INTO "tb_patterns" VALUES (79, 3, 'MTN.FNSN', 11.0, 'Middle Name Initial + dot + First Name + Second Name');
INSERT INTO "tb_patterns" VALUES (81, 3, 'MN.FNSTN', 11.0, 'Middle Name + dot + First Name + Second Name Initial');
INSERT INTO "tb_patterns" VALUES (83, 3, 'FTN_SNMN', 12.0, 'First Name Initial + underscore + Second Name + Middle Name');
INSERT INTO "tb_patterns" VALUES (85, 3, 'FN_SNMTN', 12.0, 'First Name + underscore + Second Name + Middle Name Initial');
INSERT INTO "tb_patterns" VALUES (88, 3, 'FTNSN_MN', 12.0, 'First Name Initial + Second Name + underscore + Middle Name');
INSERT INTO "tb_patterns" VALUES (90, 3, 'MTN_FNSN', 13.0, 'Middle Name Initial + underscore + First Name + Second Name');
INSERT INTO "tb_patterns" VALUES (93, 3, 'FTN_SN.MN', 14.0, 'First Name Initial + underscore + Second Name + dot + Middle Name');
INSERT INTO "tb_patterns" VALUES (95, 3, 'FTN.SN_MN', 14.0, 'First Name Initial + dot + Second Name + underscore + Middle Name');
INSERT INTO "tb_patterns" VALUES (98, 3, 'MN_FN.STN', 15.0, 'Middle Name + underscore + First Name + dot + Second Name Initial');
INSERT INTO "tb_patterns" VALUES (100, 3, 'FNSNMTX', 16.0, 'First Name + Second Name + Middle Name Letters');
INSERT INTO "tb_patterns" VALUES (102, 3, 'FTXSN.MTX', 17.0, 'First Name Letters + Second Name + dot + Middle Name Letters');
INSERT INTO "tb_patterns" VALUES (104, 3, 'FTXSN_MTX', 17.0, 'First Name Letters + Second Name + underscore + Middle Name Letters');
INSERT INTO "tb_patterns" VALUES (107, 3, 'FTX.SN_MTX', 17.0, 'First Name Letters + dot + Second Name + underscore + Middle Name Letters');
INSERT INTO "tb_patterns" VALUES (120, 4, 'MN', 1.0, 'Middle Name');
INSERT INTO "tb_patterns" VALUES (121, 4, 'LN', 1.0, 'Last Name');
INSERT INTO "tb_patterns" VALUES (123, 4, 'FNLN', 2.0, 'First Name + Last Name');
INSERT INTO "tb_patterns" VALUES (125, 4, 'FN.SN', 3.0, 'First Name + dot + Second Name');
INSERT INTO "tb_patterns" VALUES (127, 4, 'LN.FN', 3.0, 'Last Name + dot + First Name');
INSERT INTO "tb_patterns" VALUES (128, 4, 'FN_SN', 3.0, 'First Name + underscore + Second Name');
INSERT INTO "tb_patterns" VALUES (130, 4, 'LN_FN', 3.0, 'Last Name + underscore + First Name');
INSERT INTO "tb_patterns" VALUES (132, 4, 'FNSTN', 4.0, 'First Name + Second Name Initial');
INSERT INTO "tb_patterns" VALUES (134, 4, 'LTNFN', 4.0, 'Last Name Initial + First Name');
INSERT INTO "tb_patterns" VALUES (136, 4, 'FN.STN', 5.0, 'First Name + dot + Second Name Initial');
INSERT INTO "tb_patterns" VALUES (138, 4, 'LTN.FN', 5.0, 'Last Name Initial + dot + First Name');
INSERT INTO "tb_patterns" VALUES (140, 4, 'FN_STN', 5.0, 'First Name + underscore + Second Name Initial');
INSERT INTO "tb_patterns" VALUES (142, 4, 'LN_FTN', 5.0, 'Last Name + underscore + First Name Initial');
INSERT INTO "tb_patterns" VALUES (145, 4, 'FNSNLTN', 6.0, 'First Name + Second Name + Last Name Initial');
INSERT INTO "tb_patterns" VALUES (147, 4, 'FTNSTNLN', 7.0, 'First Name Initial + Second Name Initial + Last Name');
INSERT INTO "tb_patterns" VALUES (47, 3, 'MTN.FN', 5.0, 'Middle Name Initial + dot + First Name');
INSERT INTO "tb_patterns" VALUES (49, 3, 'FTN_SN', 5.0, 'First Name Initial + underscore + Second Name');
INSERT INTO "tb_patterns" VALUES (51, 3, 'FTN_MN', 5.0, 'First Name Initial + underscore + Middle Name');
INSERT INTO "tb_patterns" VALUES (53, 3, 'MTN_FN', 5.0, 'Middle Name Initial + underscore + First Name');
INSERT INTO "tb_patterns" VALUES (55, 3, 'FNSNMN', 6.0, 'First Name + Second Name + Middle Name');
INSERT INTO "tb_patterns" VALUES (57, 3, 'FN.SNMN', 7.0, 'First Name + dot + Second Name + Middle Name');
INSERT INTO "tb_patterns" VALUES (59, 3, 'MN.FNSN', 7.0, 'Middle Name + dot + First Name + Second Name');
INSERT INTO "tb_patterns" VALUES (61, 3, 'FNSN_MN', 7.0, 'First Name + Second Name + underscore + Middle Name');
INSERT INTO "tb_patterns" VALUES (63, 3, 'FN_SN.MN', 8.0, 'First Name + underscore + Second Name + dot + Middle Name');
INSERT INTO "tb_patterns" VALUES (66, 3, 'MN.FN_SN', 8.0, 'Middle Name + dot + First Name + underscore + Second Name');
INSERT INTO "tb_patterns" VALUES (68, 3, 'FTNSTNMN', 9.0, 'First Name Initial + Second Name Initial + Middle Name');
INSERT INTO "tb_patterns" VALUES (70, 3, 'MTNFNSN', 9.0, 'Middle Name Initial + First Name + Second Name');
INSERT INTO "tb_patterns" VALUES (72, 3, 'FTN.SNMN', 10.0, 'First Name Initial + dot + Second Name + Middle Name');
INSERT INTO "tb_patterns" VALUES (74, 3, 'FN.SNMTN', 10.0, 'First Name + dot + Second Name + Middle Name Initial');
INSERT INTO "tb_patterns" VALUES (32, 3, 'FN.MN', 3.0, 'First Name + dot + Middle Name');
INSERT INTO "tb_patterns" VALUES (33, 3, 'MN.FN', 3.0, 'Middle Name + dot + First Name');
INSERT INTO "tb_patterns" VALUES (35, 3, 'FN_MN', 3.0, 'First Name + underscore + Middle Name');
INSERT INTO "tb_patterns" VALUES (37, 3, 'FTNSN', 4.0, 'First Name Initial + Second Name');
INSERT INTO "tb_patterns" VALUES (38, 3, 'FNSTN', 4.0, 'First Name + Second Name Initial');
INSERT INTO "tb_patterns" VALUES (41, 3, 'MTNFN', 4.0, 'Middle Name Initial + First Name');
INSERT INTO "tb_patterns" VALUES (42, 3, 'MNFTN', 4.0, 'Middle Name + First Name Initial');
INSERT INTO "tb_patterns" VALUES (44, 3, 'FN.STN', 5.0, 'First Name + dot + Second Name Initial');
INSERT INTO "tb_patterns" VALUES (46, 3, 'FN.MTN', 5.0, 'First Name + dot + Middle Name Initial');
INSERT INTO "tb_patterns" VALUES (1, 2, 'FN', 1.0, 'First Name');
INSERT INTO "tb_patterns" VALUES (209, 4, 'LTXSNMN.FN', 21.0, 'Last Name Letters + Second Name + Middle Name + dot + First Name');
INSERT INTO "tb_patterns" VALUES (210, 4, 'LTXSTXMN.FN', 21.0, 'Last Name Letters + Second Name Letters + Middle Name + dot + First Name');
INSERT INTO "tb_patterns" VALUES (211, 4, 'FN_SNMN.LTX', 22.0, 'First Name + underscore + Second Name + Middle Name + dot + Last Name Letters');
INSERT INTO "tb_patterns" VALUES (214, 4, 'FTX_STXMTX.LN', 22.0, 'First Name Letters + underscore + Second Name Letters + Middle Name Letters + dot + Last Name');
INSERT INTO "tb_patterns" VALUES (217, 4, 'FTX.STXMN_LN', 23.0, 'First Name Letters + dot + Second Name Letters + Middle Name + underscore + Last Name');
INSERT INTO "tb_patterns" VALUES (219, 4, 'LN.SNMN_FTX', 24.0, 'Last Name + dot + Second Name + Middle Name + underscore + First Name Letters');
INSERT INTO "tb_patterns" VALUES (222, 4, 'LN_SNMN.FTX', 25.0, 'Last Name + underscore + Second Name + Middle Name + dot + First Name Letters');
INSERT INTO "tb_patterns" VALUES (2, 2, 'SN', 1.0, 'Second Name');
INSERT INTO "tb_patterns" VALUES (19, 2, 'FN.STX', 7.0, 'First Name + dot + Second Name Letters');
INSERT INTO "tb_patterns" VALUES (21, 2, 'STX.FN', 8.0, 'Second Name Letters + dot + First Name');
INSERT INTO "tb_patterns" VALUES (23, 2, 'SN.FTX', 8.0, 'Second Name + dot + First Name Letters');
INSERT INTO "tb_patterns" VALUES (26, 3, 'SN', 1.0, 'Second Name');
INSERT INTO "tb_patterns" VALUES (29, 3, 'FNMN', 2.0, 'First Name + Middle Name');
INSERT INTO "tb_patterns" VALUES (31, 3, 'FN.SN', 3.0, 'First Name + dot + Second Name');
INSERT INTO "tb_patterns" VALUES (34, 3, 'FN_SN', 3.0, 'First Name + underscore + Second Name');
INSERT INTO "tb_patterns" VALUES (36, 3, 'MN_FN', 3.0, 'Middle Name + underscore + First Name');
INSERT INTO "tb_patterns" VALUES (39, 3, 'FTNMN', 4.0, 'First Name Initial + Middle Name');
INSERT INTO "tb_patterns" VALUES (40, 3, 'FNMTN', 4.0, 'First Name + Middle Name Initial');
INSERT INTO "tb_patterns" VALUES (43, 3, 'FTN.SN', 5.0, 'First Name Initial + dot + Second Name');
INSERT INTO "tb_patterns" VALUES (45, 3, 'FTN.MN', 5.0, 'First Name Initial + dot + Middle Name');
INSERT INTO "tb_patterns" VALUES (48, 3, 'MN.FTN', 5.0, 'Middle Name + dot + First Name Initial');
INSERT INTO "tb_patterns" VALUES (50, 3, 'FN_STN', 5.0, 'First Name + underscore + Second Name Initial');
INSERT INTO "tb_patterns" VALUES (52, 3, 'FN_MTN', 5.0, 'First Name + underscore + Middle Name Initial');
INSERT INTO "tb_patterns" VALUES (54, 3, 'MN_FTN', 5.0, 'Middle Name + underscore + First Name Initial');
INSERT INTO "tb_patterns" VALUES (56, 3, 'MNFNSN', 6.0, 'Middle Name + First Name + Second Name');
INSERT INTO "tb_patterns" VALUES (58, 3, 'FNSN.MN', 7.0, 'First Name + Second Name + dot + Middle Name');
INSERT INTO "tb_patterns" VALUES (60, 3, 'FN_SNMN', 7.0, 'First Name + underscore + Second Name + Middle Name');
INSERT INTO "tb_patterns" VALUES (62, 3, 'MN_FNSN', 7.0, 'Middle Name + underscore + First Name + Second Name');
INSERT INTO "tb_patterns" VALUES (64, 3, 'FN.SN_MN', 8.0, 'First Name + dot + Second Name + underscore + Middle Name');
INSERT INTO "tb_patterns" VALUES (65, 3, 'MN_FN.SN', 8.0, 'Middle Name + underscore + First Name + dot + Second Name');
INSERT INTO "tb_patterns" VALUES (67, 3, 'FTNSNMN', 9.0, 'First Name Initial + Second Name + Middle Name');
INSERT INTO "tb_patterns" VALUES (69, 3, 'FNSNMTN', 9.0, 'First Name + Second Name + Middle Name Initial');
INSERT INTO "tb_patterns" VALUES (71, 3, 'MTNFTNSN', 9.0, 'Middle Name Initial + First Name Initial + Second Name');
INSERT INTO "tb_patterns" VALUES (73, 3, 'FTN.STNMN', 10.0, 'First Name Initial + dot + Second Name Initial + Middle Name');
INSERT INTO "tb_patterns" VALUES (75, 3, 'FTNSN.MN', 10.0, 'First Name Initial + Second Name + dot + Middle Name');
INSERT INTO "tb_patterns" VALUES (77, 3, 'FTNSN.MTN', 10.0, 'First Name Initial + Second Name + dot + Middle Name Initial');
INSERT INTO "tb_patterns" VALUES (78, 3, 'FNSTN.MTN', 10.0, 'First Name + Second Name Initial + dot + Middle Name Initial');
INSERT INTO "tb_patterns" VALUES (80, 3, 'MTN.FTNSN', 11.0, 'Middle Name Initial + dot + First Name Initial + Second Name');
INSERT INTO "tb_patterns" VALUES (82, 3, 'MTN.FNSTN', 11.0, 'Middle Name Initial + dot + First Name + Second Name Initial');
INSERT INTO "tb_patterns" VALUES (84, 3, 'FTN_STNMN', 12.0, 'First Name Initial + underscore + Second Name Initial + Middle Name');
INSERT INTO "tb_patterns" VALUES (86, 3, 'FTN_SNMTN', 12.0, 'First Name Initial + underscore + Second Name + Middle Name Initial');
INSERT INTO "tb_patterns" VALUES (109, 4, 'FN', 1.0, 'First Name');
INSERT INTO "tb_patterns" VALUES (119, 4, 'SN', 1.0, 'Second Name');
INSERT INTO "tb_patterns" VALUES (122, 4, 'FNSN', 2.0, 'First Name + Second Name');
INSERT INTO "tb_patterns" VALUES (144, 4, 'FNSNLN', 6.0, 'First Name + Second Name + Last Name');
INSERT INTO "tb_patterns" VALUES (149, 4, 'FNSN.LN', 8.0, 'First Name + Second Name + dot + Last Name');
INSERT INTO "tb_patterns" VALUES (151, 4, 'FNSN.LTN', 9.0, 'First Name + Second Name + dot + Last Name Initial');
INSERT INTO "tb_patterns" VALUES (153, 4, 'FTN.SNLN', 9.0, 'First Name Initial + dot + Second Name + Last Name');
INSERT INTO "tb_patterns" VALUES (156, 4, 'FTN.SNLTN', 10.0, 'First Name Initial + dot + Second Name + Last Name Initial');
INSERT INTO "tb_patterns" VALUES (158, 4, 'LNSNFN', 11.0, 'Last Name + Second Name + First Name');
INSERT INTO "tb_patterns" VALUES (160, 4, 'LTNSNFN', 11.0, 'Last Name Initial + Second Name + First Name');
INSERT INTO "tb_patterns" VALUES (162, 4, 'LTNSNFTN', 11.0, 'Last Name Initial + Second Name + First Name Initial');
INSERT INTO "tb_patterns" VALUES (164, 4, 'LN.SNFN', 12.0, 'Last Name + dot + Second Name + First Name');
INSERT INTO "tb_patterns" VALUES (166, 4, 'LN.SNFTN', 12.0, 'Last Name + dot + Second Name + First Name Initial');
INSERT INTO "tb_patterns" VALUES (168, 4, 'LTNSN.FN', 12.0, 'Last Name Initial + Second Name + dot + First Name');
INSERT INTO "tb_patterns" VALUES (170, 4, 'LTN.SNFTN', 12.0, 'Last Name Initial + dot + Second Name + First Name Initial');
INSERT INTO "tb_patterns" VALUES (172, 4, 'FNSNMNLN', 13.0, 'First Name + Second Name + Middle Name + Last Name');
INSERT INTO "tb_patterns" VALUES (175, 4, 'FTNSTNMNLN', 13.0, 'First Name Initial + Second Name Initial + Middle Name + Last Name');
INSERT INTO "tb_patterns" VALUES (177, 4, 'FN.SNMNLN', 14.0, 'First Name + dot + Second Name + Middle Name + Last Name');
INSERT INTO "tb_patterns" VALUES (180, 4, 'FTN.STNMNLN', 14.0, 'First Name Initial + dot + Second Name Initial + Middle Name + Last Name');
INSERT INTO "tb_patterns" VALUES (182, 4, 'FNSNMN.LN', 15.0, 'First Name + Second Name + Middle Name + dot + Last Name');
INSERT INTO "tb_patterns" VALUES (185, 4, 'FTNSTNMN.LN', 15.0, 'First Name Initial + Second Name Initial + Middle Name + dot + Last Name');
INSERT INTO "tb_patterns" VALUES (187, 4, 'LN.SNMNFN', 16.0, 'Last Name + dot + Second Name + Middle Name + First Name');
INSERT INTO "tb_patterns" VALUES (189, 4, 'LTN.SNMNFN', 16.0, 'Last Name Initial + dot + Second Name + Middle Name + First Name');
INSERT INTO "tb_patterns" VALUES (192, 4, 'LNSNMN.FN', 17.0, 'Last Name + Second Name + Middle Name + dot + First Name');
INSERT INTO "tb_patterns" VALUES (194, 4, 'LTNSNMN.FN', 17.0, 'Last Name Initial + Second Name + Middle Name + dot + First Name');
INSERT INTO "tb_patterns" VALUES (197, 4, 'FN.SNMNLTX', 18.0, 'First Name + dot + Second Name + Middle Name + Last Name Letters');
INSERT INTO "tb_patterns" VALUES (199, 4, 'FTX.STNMNLN', 18.0, 'First Name Letters + dot + Second Name Initial + Middle Name + Last Name');
INSERT INTO "tb_patterns" VALUES (201, 4, 'FNSNMN.LTX', 19.0, 'First Name + Second Name + Middle Name + dot + Last Name Letters');
INSERT INTO "tb_patterns" VALUES (204, 4, 'FTXSTXMTX.LN', 19.0, 'First Name Letters + Second Name Letters + Middle Name Letters + dot + Last Name');
INSERT INTO "tb_patterns" VALUES (207, 4, 'LTX.STXMNFN', 20.0, 'Last Name Letters + dot + Second Name Letters + Middle Name + First Name');
INSERT INTO "tb_patterns" VALUES (87, 3, 'FNSN_MTN', 12.0, 'First Name + Second Name + underscore + Middle Name Initial');
INSERT INTO "tb_patterns" VALUES (89, 3, 'FTNSN_MTN', 12.0, 'First Name Initial + Second Name + underscore + Middle Name Initial');
INSERT INTO "tb_patterns" VALUES (91, 3, 'MN_FNSTN', 13.0, 'Middle Name + underscore + First Name + Second Name Initial');
INSERT INTO "tb_patterns" VALUES (92, 3, 'MTN_FNSTN', 13.0, 'Middle Name Initial + underscore + First Name + Second Name Initial');
INSERT INTO "tb_patterns" VALUES (94, 3, 'FN_SN.MTN', 14.0, 'First Name + underscore + Second Name + dot + Middle Name Initial');
INSERT INTO "tb_patterns" VALUES (96, 3, 'FN.SN_MTN', 14.0, 'First Name + dot + Second Name + underscore + Middle Name Initial');
INSERT INTO "tb_patterns" VALUES (97, 3, 'MTN_FN.SN', 15.0, 'Middle Name Initial + underscore + First Name + dot + Second Name');
INSERT INTO "tb_patterns" VALUES (99, 3, 'FTXSNMN', 16.0, 'First Name Letters + Second Name + Middle Name');
INSERT INTO "tb_patterns" VALUES (101, 3, 'FTX.SNMN', 17.0, 'First Name Letters + dot + Second Name + Middle Name');
INSERT INTO "tb_patterns" VALUES (103, 3, 'FTX_SNMN', 17.0, 'First Name Letters + underscore + Second Name + Middle Name');
INSERT INTO "tb_patterns" VALUES (105, 3, 'FTX_SN.MN', 17.0, 'First Name Letters + underscore + Second Name + dot + Middle Name');
INSERT INTO "tb_patterns" VALUES (106, 3, 'FTX.SN_MN', 17.0, 'First Name Letters + dot + Second Name + underscore + Middle Name');
INSERT INTO "tb_patterns" VALUES (108, 3, 'FTX_SN.MTX', 17.0, 'First Name Letters + underscore + Second Name + dot + Middle Name Letters');
INSERT INTO "tb_patterns" VALUES (124, 4, 'LNFN', 2.0, 'Last Name + First Name');
INSERT INTO "tb_patterns" VALUES (126, 4, 'FN.LN', 3.0, 'First Name + dot + Last Name');
INSERT INTO "tb_patterns" VALUES (129, 4, 'FN_LN', 3.0, 'First Name + underscore + Last Name');
INSERT INTO "tb_patterns" VALUES (131, 4, 'FTNSN', 4.0, 'First Name Initial + Second Name');
INSERT INTO "tb_patterns" VALUES (133, 4, 'LNFTN', 4.0, 'Last Name + First Name Initial');
INSERT INTO "tb_patterns" VALUES (135, 4, 'FTN.SN', 5.0, 'First Name Initial + dot + Second Name');
INSERT INTO "tb_patterns" VALUES (137, 4, 'LN.FTN', 5.0, 'Last Name + dot + First Name Initial');
INSERT INTO "tb_patterns" VALUES (139, 4, 'FTN_SN', 5.0, 'First Name Initial + underscore + Second Name');
INSERT INTO "tb_patterns" VALUES (141, 4, 'FTN_LN', 5.0, 'First Name Initial + underscore + Last Name');
INSERT INTO "tb_patterns" VALUES (143, 4, 'LTN_FN', 5.0, 'Last Name Initial + underscore + First Name');
INSERT INTO "tb_patterns" VALUES (146, 4, 'FTNSNLN', 6.0, 'First Name Initial + Second Name + Last Name');
INSERT INTO "tb_patterns" VALUES (148, 4, 'FTNSNLTN', 7.0, 'First Name Initial + Second Name + Last Name Initial');
INSERT INTO "tb_patterns" VALUES (150, 4, 'FN.SNLN', 8.0, 'First Name + dot + Second Name + Last Name');
INSERT INTO "tb_patterns" VALUES (152, 4, 'FN.SNLTN', 9.0, 'First Name + dot + Second Name + Last Name Initial');
INSERT INTO "tb_patterns" VALUES (154, 4, 'FTNSN.LN', 9.0, 'First Name Initial + Second Name + dot + Last Name');
INSERT INTO "tb_patterns" VALUES (155, 4, 'FTN.STNLN', 10.0, 'First Name Initial + dot + Second Name Initial + Last Name');
INSERT INTO "tb_patterns" VALUES (157, 4, 'FTNSN.LTN', 10.0, 'First Name Initial + Second Name + dot + Last Name Initial');
INSERT INTO "tb_patterns" VALUES (159, 4, 'LNSNFTN', 11.0, 'Last Name + Second Name + First Name Initial');
INSERT INTO "tb_patterns" VALUES (161, 4, 'LTNSTNFN', 11.0, 'Last Name Initial + Second Name Initial + First Name');
INSERT INTO "tb_patterns" VALUES (163, 4, 'LNSN.FN', 12.0, 'Last Name + Second Name + dot + First Name');
INSERT INTO "tb_patterns" VALUES (165, 4, 'LNSN.FTN', 12.0, 'Last Name + Second Name + dot + First Name Initial');
INSERT INTO "tb_patterns" VALUES (167, 4, 'LTN.SNFN', 12.0, 'Last Name Initial + dot + Second Name + First Name');
INSERT INTO "tb_patterns" VALUES (169, 4, 'LTN.STNFN', 12.0, 'Last Name Initial + dot + Second Name Initial + First Name');
INSERT INTO "tb_patterns" VALUES (171, 4, 'LTNSN.FTN', 12.0, 'Last Name Initial + Second Name + dot + First Name Initial');
INSERT INTO "tb_patterns" VALUES (173, 4, 'FNSNMNLTN', 13.0, 'First Name + Second Name + Middle Name + Last Name Initial');
INSERT INTO "tb_patterns" VALUES (174, 4, 'FTNSNMNLN', 13.0, 'First Name Initial + Second Name + Middle Name + Last Name');
INSERT INTO "tb_patterns" VALUES (176, 4, 'FTNSTNMTNLN', 13.0, 'First Name Initial + Second Name Initial + Middle Name Initial + Last Name');
INSERT INTO "tb_patterns" VALUES (178, 4, 'FN.SNMNLTN', 14.0, 'First Name + dot + Second Name + Middle Name + Last Name Initial');
INSERT INTO "tb_patterns" VALUES (179, 4, 'FTN.SNMNLN', 14.0, 'First Name Initial + dot + Second Name + Middle Name + Last Name');
INSERT INTO "tb_patterns" VALUES (181, 4, 'FTN.STNMTNLN', 14.0, 'First Name Initial + dot + Second Name Initial + Middle Name Initial + Last Name');
INSERT INTO "tb_patterns" VALUES (183, 4, 'FNSNMN.LTN', 15.0, 'First Name + Second Name + Middle Name + dot + Last Name Initial');
INSERT INTO "tb_patterns" VALUES (184, 4, 'FTNSNMN.LN', 15.0, 'First Name Initial + Second Name + Middle Name + dot + Last Name');
INSERT INTO "tb_patterns" VALUES (186, 4, 'FTNSTNMTN.LN', 15.0, 'First Name Initial + Second Name Initial + Middle Name Initial + dot + Last Name');
INSERT INTO "tb_patterns" VALUES (188, 4, 'LN.SNMNFTN', 16.0, 'Last Name + dot + Second Name + Middle Name + First Name Initial');
INSERT INTO "tb_patterns" VALUES (190, 4, 'LTN.STNMNFN', 16.0, 'Last Name Initial + dot + Second Name Initial + Middle Name + First Name');
INSERT INTO "tb_patterns" VALUES (191, 4, 'LTN.STNMTNFN', 16.0, 'Last Name Initial + dot + Second Name Initial + Middle Name Initial + First Name');
INSERT INTO "tb_patterns" VALUES (193, 4, 'LNSNMN.FTN', 17.0, 'Last Name + Second Name + Middle Name + dot + First Name Initial');
INSERT INTO "tb_patterns" VALUES (195, 4, 'LTNSTNMN.FN', 17.0, 'Last Name Initial + Second Name Initial + Middle Name + dot + First Name');
INSERT INTO "tb_patterns" VALUES (196, 4, 'LTNSTNMTN.FN', 17.0, 'Last Name Initial + Second Name Initial + Middle Name Initial + dot + First Name');
INSERT INTO "tb_patterns" VALUES (198, 4, 'FTX.SNMNLN', 18.0, 'First Name Letters + dot + Second Name + Middle Name + Last Name');
INSERT INTO "tb_patterns" VALUES (200, 4, 'FTX.STNMTNLN', 18.0, 'First Name Letters + dot + Second Name Initial + Middle Name Initial + Last Name');
INSERT INTO "tb_patterns" VALUES (202, 4, 'FTXSNMN.LN', 19.0, 'First Name Letters + Second Name + Middle Name + dot + Last Name');
INSERT INTO "tb_patterns" VALUES (203, 4, 'FTXSTXMN.LN', 19.0, 'First Name Letters + Second Name Letters + Middle Name + dot + Last Name');
INSERT INTO "tb_patterns" VALUES (205, 4, 'LN.SNMNFTX', 20.0, 'Last Name + dot + Second Name + Middle Name + First Name Letters');
INSERT INTO "tb_patterns" VALUES (206, 4, 'LTX.SNMNFN', 20.0, 'Last Name Letters + dot + Second Name + Middle Name + First Name');
INSERT INTO "tb_patterns" VALUES (208, 4, 'LNSNMN.FTX', 21.0, 'Last Name + Second Name + Middle Name + dot + First Name Letters');
INSERT INTO "tb_patterns" VALUES (212, 4, 'FTX_SNMN.LN', 22.0, 'First Name Letters + underscore + Second Name + Middle Name + dot + Last Name');
INSERT INTO "tb_patterns" VALUES (213, 4, 'FTX_STXMN.LN', 22.0, 'First Name Letters + underscore + Second Name Letters + Middle Name + dot + Last Name');
INSERT INTO "tb_patterns" VALUES (215, 4, 'FN.SNMN_LTX', 23.0, 'First Name + dot + Second Name + Middle Name + underscore + Last Name Letters');
INSERT INTO "tb_patterns" VALUES (216, 4, 'FTX.SNMN_LN', 23.0, 'First Name Letters + dot + Second Name + Middle Name + underscore + Last Name');
INSERT INTO "tb_patterns" VALUES (217, 2, 'STX_FTX', 9.0, 'Second Name Letters + underscore + First Name Letters');
INSERT INTO "tb_patterns" VALUES (218, 2, 'FTX_STX', 9.0, 'First Name Letters + underscore + Second Name Letters');
INSERT INTO "tb_patterns" VALUES (219, 2, 'STX.FTX', 9.0, 'Second Name Letters + dot+ First Name Letters');
INSERT INTO "tb_patterns" VALUES (220, 2, 'FTX.STX', 9.0, 'First Name Letters + dot + Second Name Letters');
INSERT INTO "tb_patterns" VALUES (221, 2, 'STXFTX', 9.0, 'Second Name Letters + First Name Letters');
INSERT INTO "tb_patterns" VALUES (222, 2, 'FTXSTX', 9.0, 'First Name Letters + Second Name Letters');
INSERT INTO "tb_patterns" VALUES (223, 2, 'STX-FTX', 9.0, 'Second Name Letters + dash + First Name Letters');
INSERT INTO "tb_patterns" VALUES (224, 2, 'FTX-STX', 9.0, 'First Name Letters + dash+ Second Name Letters');

PRAGMA foreign_keys = true;