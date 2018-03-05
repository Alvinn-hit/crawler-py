
drop table T_TS_IMPACT_FACTOR_HIS;
  CREATE TABLE "T_TS_IMPACT_FACTOR_HIS" 
   (	
    "FID" NUMBER NOT NULL ENABLE, 
	"IMPACT_RANGE" VARCHAR2(50 BYTE) NOT NULL ENABLE, 
	"MONTH" VARCHAR2(255 BYTE) NOT NULL ENABLE, 
	"VALUE" FLOAT(126), 
	"UPDATER" VARCHAR2(50 BYTE), 
	"UPDATETIME" TIMESTAMP (6) DEFAULT CURRENT_TIMESTAMP, 
	 CONSTRAINT "T_TS_IMPACT_FACTOR_HIS_PK" PRIMARY KEY ("FID", "MONTH")
   );
 
   COMMENT ON COLUMN "T_TS_IMPACT_FACTOR_HIS"."IMPACT_RANGE" IS '影响范围';
 
   COMMENT ON COLUMN "T_TS_IMPACT_FACTOR_HIS"."MONTH" IS '年月';
 
   COMMENT ON COLUMN "T_TS_IMPACT_FACTOR_HIS"."UPDATER" IS '修改者';
 
   COMMENT ON COLUMN "T_TS_IMPACT_FACTOR_HIS"."UPDATETIME" IS '入库时间';
 





/*
drop table original_data;
drop sequence original_data_sequence;
create table original_data(
  id number primary key ,
  name_index number ,
  name varchar2(2000) NOT NULL,
  data_date date ,
  year number ,
  month number ,
  value number NOT NULL,
  unit varchar2(20) ,
  data_type number  ,
  create_time timestamp
);

COMMENT ON COLUMN original_data.data_type IS '1、按月社会消费品零售总额_当期值;2、按月进口总值_当期值、按月出口总值_当期值;3、民航货运量_当期值;;4、按月国内航线货邮运输量、国际航线货邮运输量;5、WTI原油价格';

CREATE SEQUENCE original_data_sequence
    INCREMENT BY 1  -- 每次加几个
    START WITH 1    -- 从1开始计数
    NOMAXVALUE      -- 不设置最大值
    NOCYCLE         -- 一直累加，不循环
    CACHE 10;
    
*/  