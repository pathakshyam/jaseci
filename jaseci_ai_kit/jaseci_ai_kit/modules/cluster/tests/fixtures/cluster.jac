walker test_umap {
    can use.encode;
    can cluster.get_umap;

    encodes = use.encode(["still waiting card",
        "countries supporting",
        "card still arrived weeks",
        "countries accounts suppor",
        "provide support countries",
        "waiting week card still coming",
        "track card process delivery",
        "countries getting support",
        "know get card lost",
        "send new card",
        "still received new card",
        "info card delivery",
        "new card still come",
        "way track delivery card",
        "countries currently support"
        ]);

    report cluster.get_umap(encodes,2);
}

walker test_get_cluster {
    can cluster.get_cluster_labels;
    embedds = [[24.610413,2.7083237],[ 9.004074, 12.092478 ],[24.0603,3.5194352],
                [ 9.301909,12.320379 ],[ 8.598204, 11.284211 ],[24.364273,3.1760032],
                [ 4.79636,5.1774173],[ 8.819081,11.591265],[24.452982,2.4640806],
                [ 2.793474,8.419835 ],[2.1980357,7.805085 ],[ 5.394445,4.5522223],
                [ 2.5296957,8.163622 ],[ 5.1212783,4.836675 ],[ 9.165633,11.404499 ]];
    report cluster.get_cluster_labels(embedds,"hbdscan",2,2);
}