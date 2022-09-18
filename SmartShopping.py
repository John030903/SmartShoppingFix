import streamlit as st
import requests
import json
import numpy as np
from numerize import numerize

def LoadDataFromWeb(url):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42',
              'Referer':'https://shopee.vn/'}
    response = requests.get(url, headers=headers)
    st.write(response.status_code)
    data = json.loads(response.content)
    return data
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)  
     
local_css("Style.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')
class Standards:
  thumbnail_url = ""
  clickUrl = ""
  name = ""
  rating_average = 0
  sold = 0
  price = 0

def ShopeeFilter(item):
  standard = Standards()
  item_basic = item["item_basic"]
  linkImg = "https://cf.shopee.vn/file/{imgid}_tn"
  path = "https://shopee.vn/Tên tôi là Nguyễn Hoàng Khánh Duy-i.{shopid}.{itemid}?sp_atk=fe04f1e4-5cb6-440b-82fa-c2ec03fc36dd&xptdk=fe04f1e4-5cb6-440b-82fa-c2ec03fc36dd"
  standard.clickUrl = path.format(shopid=item_basic["shopid"], itemid=item_basic["itemid"])
  standard.thumbnail_url = linkImg.format(imgid = item_basic["image"])
  standard.name = item_basic["name"]
  standard.rating_average = item_basic["item_rating"]["rating_star"]
  standard.sold = item_basic["historical_sold"]
  strPrice = str(item_basic["price"])[:-5]
  standard.price = int(strPrice)
  return standard
def LazadaFilter(item):
  try:
    standard = Standards()
    path = "https://www.lazada.vn/{}"
    thumbs0 = item["thumbs"][0]
    standard.clickUrl = path.format(thumbs0["itemUrl"])
    standard.thumbnail_url = thumbs0["image"]
    standard.rating_average = item["ratingScore"]
    standard.name = item["name"]
    standard.price = int(float(item["price"]))
    if item["review"] == "":
      standard.sold = 0
    else: 
      standard.sold = int(int(item["review"])/0.3361)
  except:
    standard = ShopeeFilter(item)
  return standard

def TikiFilter(item):
  try:
    standard = Standards()
    path = "https://tiki.vn/{}"
    standard.clickUrl = path.format(item["url_path"])
    standard.thumbnail_url = item["thumbnail_url"]
    standard.rating_average = item["rating_average"]
    standard.name = item["name"]
    standard.price = item["price"]
    try:
      standard.sold = item["quantity_sold"]["value"]
    except:
      standard.sold = 0
  except:
    standard = LazadaFilter(item)
  return standard
st.image("Icon.png")
key = st.text_input(label="",placeholder="Nhập tên sản phẩm", key="Search")
if st.session_state.Search:
  TIKI_SEARCH = "https://tiki.vn/api/v2/products?limit=48&include=advertisement&aggregations=2&trackity_id=a818abb0-b29b-a7e7-c95b-bfa1603a6b24&q={}&sort=top_seller"
  LAZADA_SEARCH = "https://www.lazada.vn/catalog/?_keyori=ss&ajax=true&from=input&isFirstRequest=true&page=1&q={}&spm=a2o4n.searchlist.search.go.5e594c25s1bBVU"
  SHOPEE_SEARCH = "https://shopee.vn/api/v4/search/search_items?by=sales&keyword={}&limit=60&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2"
  # tikiData = LoadDataFromWeb(TIKI_SEARCH.format(key))
  # lazadaData = LoadDataFromWeb(LAZADA_SEARCH.format(key))
  shopeeData = LoadDataFromWeb(SHOPEE_SEARCH.format(key))

  # tikiItems = np.array(tikiData["data"])
  # lazadaItems = np.array(lazadaData["mods"]["listItems"])
#   shopeeItems = np.array(shopeeData["items"])
  # items = sorted(tikiData["data"]+lazadaData["mods"]["listItems"]+shopeeData["items"], key=lambda x: float(x["price"]))
  # items = tikiData["data"]+lazadaData["mods"]["listItems"]+shopeeData["items"]
  items = shopeeData["items"]
  row0 = """<div
    data-view-id="product_list_container"
    class="ProductList__Wrapper-sc-1dl80l2-0 Kxajl">"""
  col = """<a
    class="product-item"
    href= "{clickUrl}"
    data-view-index="0"
    data-view-id="product_list_item"
    rel="nofollow"
    style="height: 100%"
  >
    <div class="style__StyledItem-sc-18svp8n-0 fkDgwT">
      <div class="thumbnail">
        <img src= "{linkImg}" />
      </div>
      <div class="info">
        <div class="name">
          <span> {name} </span>
        </div>
        <div
          class="styles__StyledRatingQtySold-sc-732h27-0 uDeVr"
          style="margin-top: 2px; margin-bottom: 2px"
        >
          <div class="full-rating">
            <div class="total">
              <svg
                stroke="currentColor"
                fill="currentColor"
                stroke-width="0"
                viewBox="0 0 24 24"
                size="14"
                color="#c7c7c7"
                height="14"
                width="14"
                xmlns="http://www.w3.org/2000/svg"
                style="color: rgb(199, 199, 199)"
              >
                <path
                  d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"
                ></path>
              </svg>
              <svg
                stroke="currentColor"
                fill="currentColor"
                stroke-width="0"
                viewBox="0 0 24 24"
                size="14"
                color="#c7c7c7"
                height="14"
                width="14"
                xmlns="http://www.w3.org/2000/svg"
                style="color: rgb(199, 199, 199)"
              >
                <path
                  d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"
                ></path>
              </svg>
              <svg
                stroke="currentColor"
                fill="currentColor"
                stroke-width="0"
                viewBox="0 0 24 24"
                size="14"
                color="#c7c7c7"
                height="14"
                width="14"
                xmlns="http://www.w3.org/2000/svg"
                style="color: rgb(199, 199, 199)"
              >
                <path
                  d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"
                ></path>
              </svg>
              <svg
                stroke="currentColor"
                fill="currentColor"
                stroke-width="0"
                viewBox="0 0 24 24"
                size="14"
                color="#c7c7c7"
                height="14"
                width="14"
                xmlns="http://www.w3.org/2000/svg"
                style="color: rgb(199, 199, 199)"
              >
                <path
                  d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"
                ></path>
              </svg>
              <svg
                stroke="currentColor"
                fill="currentColor"
                stroke-width="0"
                viewBox="0 0 24 24"
                size="14"
                color="#c7c7c7"
                height="14"
                width="14"
                xmlns="http://www.w3.org/2000/svg"
                style="color: rgb(199, 199, 199)"
              >
                <path
                  d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"
                ></path>
              </svg>
            </div>
            <div class="average" style="width: {rating:.0%}">
              <svg
                stroke="currentColor"
                fill="currentColor"
                stroke-width="0"
                viewBox="0 0 24 24"
                size="14"
                color="#fdd836"
                height="14"
                width="14"
                xmlns="http://www.w3.org/2000/svg"
                style="color: rgb(253, 216, 54)"
              >
                <path
                  d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"
                ></path>
              </svg>
              <svg
                stroke="currentColor"
                fill="currentColor"
                stroke-width="0"
                viewBox="0 0 24 24"
                size="14"
                color="#fdd836"
                height="14"
                width="14"
                xmlns="http://www.w3.org/2000/svg"
                style="color: rgb(253, 216, 54)"
              >
                <path
                  d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"
                ></path>
              </svg>
              <svg
                stroke="currentColor"
                fill="currentColor"
                stroke-width="0"
                viewBox="0 0 24 24"
                size="14"
                color="#fdd836"
                height="14"
                width="14"
                xmlns="http://www.w3.org/2000/svg"
                style="color: rgb(253, 216, 54)"
              >
                <path
                  d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"
                ></path>
              </svg>
              <svg
                stroke="currentColor"
                fill="currentColor"
                stroke-width="0"
                viewBox="0 0 24 24"
                size="14"
                color="#fdd836"
                height="14"
                width="14"
                xmlns="http://www.w3.org/2000/svg"
                style="color: rgb(253, 216, 54)"
              >
                <path
                  d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"
                ></path>
              </svg>
              <svg
                stroke="currentColor"
                fill="currentColor"
                stroke-width="0"
                viewBox="0 0 24 24"
                size="14"
                color="#fdd836"
                height="14"
                width="14"
                xmlns="http://www.w3.org/2000/svg"
                style="color: rgb(253, 216, 54)"
              >
                <path
                  d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"
                ></path>
              </svg>
            </div>
          </div>
          <div class="styles__StyledSeparator-sc-732h27-1 gcwbHk"></div>
          <div class="styles__StyledQtySold-sc-732h27-2 fCfYNm">Đã bán {sold}</div>
        </div>
      </div>
      <div class="price"> {price} đ</div>
    </div>
  </a>"""
  def FormatPrice(price):
    price = str(price)
    for i in range(len(price)-3,-1,-3):
      if i != 0:
        price = price[:i] + "." + price[i:]
    return price
  for item in items:
    sd = ShopeeFilter(item)
    if sd.sold == 0 or float(sd.rating_average) < 4: continue
    rating_average = float(sd.rating_average)/5
    row0 += col.format(clickUrl=sd.clickUrl,linkImg=sd.thumbnail_url,name=sd.name,sold=numerize.numerize(int(sd.sold)),rating=rating_average,price=FormatPrice(sd.price))
  row0 += "</div>"
  st.markdown(row0,unsafe_allow_html= True)
