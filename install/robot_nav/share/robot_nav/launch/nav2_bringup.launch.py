import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution


def generate_launch_description():
    pkg_share = get_package_share_directory('robot_nav')

    map_file = os.path.join(
        pkg_share,
        'map',
        'turtlebot3_world_map.yaml'
    )

    amcl_config = os.path.join(
        pkg_share,
        'config',
        'amcl.yaml'
    )

    planner_config = os.path.join(
        pkg_share,
        'config',
        'planner_server.yaml'
    )

    global_costmap_config = os.path.join(
        pkg_share,
        'config',
        'global_costmap.yaml'
    )

    controller_config = os.path.join(
        pkg_share,
        'config',
        'controller_server.yaml'
    )

    local_costmap_config = os.path.join(
        pkg_share,
        'config',
        'local_costmap.yaml'
    )

    behavior_config = os.path.join(
        pkg_share,
        'config',
        'behavior_server.yaml'
    )

    bt_navigator_config = os.path.join(
        pkg_share,
        'config',
        'bt_navigator.yaml'
    )

    rviz_config_path = PathJoinSubstitution([
        FindPackageShare('robot_nav'),
        'rviz',
        'nav2.rviz'
    ])

    lifecycle_nodes = [
        'map_server',
        'amcl',
        'planner_server',
        'controller_server',
        'behavior_server',
        'bt_navigator'
    ]

    map_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[
            {'use_sim_time': True},
            {'yaml_filename': map_file}
        ]
    )

    amcl = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[
            amcl_config
        ]
    )

    planner_server = Node(
        package='nav2_planner',
        executable='planner_server',
        name='planner_server',
        output='screen',
        parameters=[
            planner_config,
            global_costmap_config
        ]
    )

    controller_server = Node(
        package='nav2_controller',
        executable='controller_server',
        name='controller_server',
        output='screen',
        parameters=[
            controller_config,
            local_costmap_config
        ]
    )

    behavior_server = Node(
        package='nav2_behaviors',
        executable='behavior_server',
        name='behavior_server',
        output='screen',
        parameters=[
            behavior_config
        ]
    )

    bt_navigator = Node(
        package='nav2_bt_navigator',
        executable='bt_navigator',
        name='bt_navigator',
        output='screen',
        parameters=[
            bt_navigator_config
        ]
    )

    lifecycle_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_navigation',
        output='screen',
        parameters=[
            {'use_sim_time': True},
            {'autostart': True},
            {'node_names': lifecycle_nodes}
        ]
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_path],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    return LaunchDescription([
        map_server,
        amcl,
        planner_server,
        controller_server,
        behavior_server,
        bt_navigator,
        lifecycle_manager,
        rviz_node
    ])