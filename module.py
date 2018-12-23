#!python3
import xml.etree.ElementTree as et
import folium
import pandas as pd

def parse_csv(file="data/gurume.csv"):
    # お店csv読み込み
    df = pd.read_csv(file, encoding="cp932")
    # .osmから表示緯度経度取得
    import xml.etree.ElementTree as et
    tree = et.parse("data/map.osm")
    root = tree.getroot()

    maxlat = float(root[0].get("maxlat"))
    maxlon = float(root[0].attrib["maxlon"])
    minlat = float(root[0].attrib["minlat"])
    minlon = float(root[0].attrib["minlon"])
    # dfから範囲内の緯度経度を持つ行を取得
    shops = df[((df.lng > float(minlon)) & (df.lng < float(maxlon))) & ((df.lat > float(minlat)) & (df.lat < float(maxlat)))]
    data = shops[["name", "genre", "score", "lat", "lng"]]
    return (minlat, minlon, maxlat, maxlon), data
    
def parse_osm(filename="data/map.osm"):
    tree = et.parse(filename)
    root = tree.getroot()

    # 表示緯度経度取得
    maxlat = float(root[0].get("maxlat"))
    maxlon = float(root[0].attrib["maxlon"])
    minlat = float(root[0].attrib["minlat"])
    minlon = float(root[0].attrib["minlon"])
    maxlat

    # cuisine
    names = []
    lats = []
    lons = []
    for node in root.iter("node"):
        is_shop = False
        name = None
        for tag in node.iter("tag"):
            if tag.get("k")=="cuisine":
                is_shop = True
            if tag.get("k")=="name":
                name = tag.get("v")
        if is_shop:
            names.append(name)
            lats.append(float(node.get("lat")))
            lons.append(float(node.get("lon")))

    return (minlat, minlon, maxlat, maxlon), (names, lats, lons)

def folium_map(loc, names, lats, lons, scores=None, genres=None):
    """
    loc = (minlat, minlon, maxlat, maxlon)で指定する範囲に
    names の名前のマーカーをlats, lonsの位置に表示
    """
    # 地図取得
    lat = (loc[0]+loc[2])/2 # 緯度
    lon = (loc[1]+loc[3])/2 # 経度
    m = folium.Map(location=[lat, lon], zoom_start=15)
    
    # マーカー
    for ind, (name, lat, lon) in enumerate(zip(names, lats, lons)):
        if ind>200:
            break
        if scores is not None:
            popup = "genre: %s\nscore: %f" % (genres.iloc[ind], scores.iloc[ind])
            score = scores.iloc[ind]
            if score > scores.quantile(0.75):
                color = "red"
            elif score < scores.quantile(0.25):
                color = "blue"
            else:
                color = "green"
            icon = folium.Icon(color=color)
            marker = folium.Marker([lat, lon], popup=popup, tooltip=name, icon=icon)
        else:
            popup = name
            marker = folium.Marker([lat, lon], popup=popup, tooltip=name)
        marker.add_to(m)
    return m
# loc, (names, lats, lons) = parse_osm()
loc, data = parse_csv()
names = data["name"]
lats = data["lat"]
lons = data["lng"]
scores = data["score"]
genres = data["genre"]
m = folium_map(loc, names, lats, lons, scores, genres)