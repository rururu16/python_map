import pandas as pd
import xml.etree.ElementTree as ET
import folium

tree = ET.parse("data/map.osm")
root = tree.getroot()
d = root[0].attrib

# map.osmの範囲
minlat = float(d["minlat"])
minlon = float(d["minlon"])
maxlat = float(d["maxlat"])
maxlon = float(d["maxlon"])

# お店リストcsv
file = "data/gurume.csv"
df = pd.read_csv(file, encoding="cp932")

b1 = (df["lng"] > minlon) & (df["lng"] < maxlon)
b2 = (df["lat"] > minlat) & (df["lat"] < maxlat)
ind = b1 & b2

# boolがtrueの列を取得
shops = df[ind]

# 四分位点の取得
qs = shops["score"].quantile([0.25, 0.75])
high = qs[0.75]
low = qs[0.25]

# スコアに応じた表示色
shops = shops.assign(color="green")
highInd = shops.score > high
lowInd = shops.score < low
shops.loc[highInd, "color"] = "red"
shops.loc[lowInd, "color"] = "blue"

shops["genre_new"] = shops["genre"].str.split("'", expand=True)[7]

lat = (minlat + maxlat) / 2
lon = (minlon + maxlon) / 2

m = folium.Map(location=[lat, lon], zoom_start=16)
for i in range(shops.shape[0]):
    icon =  folium.Icon(color=shops["color"].iloc[i])
    genre = shops["genre_new"].iloc[i]
    score = shops["score"].iloc[i]
    marker = folium.Marker([shops["lat"].iloc[i], shops["lng"].iloc[i]],
                            icon=icon,
                            tooltip=shops["name"].iloc[i],
                            popup="ジャンル: %s <br> 食べログ: %s" % (genre, score))
    marker.add_to(m)

m.save('data/rukamap.html')