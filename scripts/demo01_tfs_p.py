#! /usr/bin/env/python

import rospy
import tf2_ros
from tf2_geometry_msgs import tf2_geometry_msgs
from geometry_msgs.msg import TransformStamped

if __name__ == "__main__":    

    # 2.初始化
    rospy.init_node("static_sub_p")
    # 3.创建订阅对象
    # 3-1.创建缓存对象
    buffer = tf2_ros.Buffer()
    # 3-2.创建订阅对象（将缓存对象传入）
    sub = tf2_ros.TransformListener(buffer)  
    # 4.组织被转化的坐标点
    ps = tf2_geometry_msgs.PointStamped()
    #时间戳 -- 0
    # ps.header.stamp = rospy.Time()
    ps.header.stamp = rospy.Time.now()
    # 坐标系
    ps.header.frame_id = "son1"     
    ps.point.x = 1.0
    ps.point.y = 2.0
    ps.point.z = 3.0
    # 5.转换逻辑实现，调用tf封装的算法
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        try:       
            # ----- 计算 son1 相对于 son2 的坐标关系
            """
                参数1 ：目标坐标系
                参数2 ：源坐标系
                参数3 ：rospy.Time(0) --- 取时间间隔最近的两个坐标系帧（son1 相对 world 与 son2 相对 world）
                返回值 ： son1 与 son2 的坐标系关系；           
            """
            ts = buffer.lookup_transform("son2","son1",rospy.Time(0))
            rospy.loginfo("父级坐标系:%s,子级坐标系:%s",
                    ts.header.frame_id,
                    ts.child_frame_id
                    )
    
            # 转换实现
            ps_out = buffer.transform(ps,"son2",rospy.Duration(0.5))
            # 6.输出结果
            rospy.loginfo("转换后的坐标：(%.2f,%.2f,%.2f),参考的坐标系：%s",
                        ps_out.point.x,
                        ps_out.point.y,
                        ps_out.point.z,
                        ps_out.header.frame_id
                        )
        except Exception as e:
            rospy.logwarn("错误提示：%s",e)
        
        # 7.spin() | spinOnce()
        rate.sleep()