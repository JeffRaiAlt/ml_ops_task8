from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.queue import Kafka
from diagrams.onprem.compute import Server
from diagrams.onprem.analytics import Spark
from diagrams.onprem.network import Nginx
from diagrams.onprem.monitoring import Grafana

import os

os.environ["PATH"] += os.pathsep + 'C:/IDE/Graphviz/bin/'

graph_attr = {
    "fontsize": "18",
    "bgcolor": "white",
    "pad": "0.6",
    "splines": "ortho",
    "nodesep": "0.8",
    "ranksep": "1.2",
}

with Diagram(
    "Virtual Product Placement — Kappa Architecture",
    filename="vpp_simple",
    direction="LR",
    show=False,
    graph_attr=graph_attr,
):
    # Источники (один узел-агрегат)
    sources = Server("Sources\n(viewer · video · campaign)")

    # Единый event log
    event_log = Kafka("Event Log\n(Kafka)")

    # Онлайн-контур
    with Cluster("Online Path"):
        decision = Server("Ad Decision")
        rendering = Server("GPU Rendering")
        packager  = Nginx("CDN Packager")

    # Offline-контур
    with Cluster("Offline Path  [replay from log]"):
        ml_train = Spark("Model Training\n(CV · ranking · brand-safety)")
        inventory = Server("Scene Inventory")

    # Доставка
    viewer = Server("Viewer")

    #  Мониторинг
    monitoring = Grafana("Monitoring")

    # Основной поток
    sources   >> Edge(color="#555555") >> event_log
    event_log >> Edge(color="#2266cc") >> decision
    decision  >> Edge(color="#2266cc") >> rendering
    rendering >> Edge(color="#2266cc") >> packager
    packager  >> Edge(color="#cc4422", label="personalized video") >> viewer

    # Offline: replay из лога
    event_log >> Edge(style="dashed", color="#338833", label="replay") >> ml_train
    ml_train  >> Edge(style="dashed", color="#338833") >> inventory

    # Offline → Online: деплой моделей и слотов
    ml_train  >> Edge(style="dashed", color="#338833", label="deploy models") >> rendering
    inventory >> Edge(style="dashed", color="#338833", label="available slots") >> decision

    # Мониторинг
    rendering >> Edge(style="dotted", color="#aa8800") >> monitoring