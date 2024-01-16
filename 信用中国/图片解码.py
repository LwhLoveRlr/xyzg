# -*- coding: utf-8 -*-

import base64
import re
import uuid


def decode_image(src):
    """
    解码图片
    :param src: 图片编码
        eg:
            src="data:image/gif;base64,R0lGODlhMwAxAIAAAAAAAP///
                yH5BAAAAAAALAAAAAAzADEAAAK8jI+pBr0PowytzotTtbm/DTqQ6C3hGX
                ElcraA9jIr66ozVpM3nseUvYP1UEHF0FUUHkNJxhLZfEJNvol06tzwrgd
                LbXsFZYmSMPnHLB+zNJFbq15+SOf50+6rG7lKOjwV1ibGdhHYRVYVJ9Wn
                k2HWtLdIWMSH9lfyODZoZTb4xdnpxQSEF9oyOWIqp6gaI9pI1Qo7BijbF
                ZkoaAtEeiiLeKn72xM7vMZofJy8zJys2UxsCT3kO229LH1tXAAAOw=="

    :return: str 保存到本地的文件名
    """
    # 1、信息提取
    result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", src, re.DOTALL)
    if result:
        ext = result.groupdict().get("ext")
        data = result.groupdict().get("data")

    else:
        raise Exception("Do not parse!")

    # 2、base64解码
    img = base64.urlsafe_b64decode(data)

    # 3、二进制文件保存
    filename = "{}.{}".format("验证码", 'jpg')
    with open(filename, "wb") as f:
        f.write(img)

    return filename


def encode_image(filename):
    """
    编码图片
    :param filename: str 本地图片文件名
    :return: str 编码后的字符串
        eg:
        src="data:image/gif;base64,R0lGODlhMwAxAIAAAAAAAP///
            yH5BAAAAAAALAAAAAAzADEAAAK8jI+pBr0PowytzotTtbm/DTqQ6C3hGX
            ElcraA9jIr66ozVpM3nseUvYP1UEHF0FUUHkNJxhLZfEJNvol06tzwrgd
            LbXsFZYmSMPnHLB+zNJFbq15+SOf50+6rG7lKOjwV1ibGdhHYRVYVJ9Wn
            k2HWtLdIWMSH9lfyODZoZTb4xdnpxQSEF9oyOWIqp6gaI9pI1Qo7BijbF
            ZkoaAtEeiiLeKn72xM7vMZofJy8zJys2UxsCT3kO229LH1tXAAAOw=="

    """
    # 1、文件读取
    ext = filename.split(".")[-1]

    with open(filename, "rb") as f:
        img = f.read()

    # 2、base64编码
    data = base64.b64encode(img).decode()

    # 3、图片编码字符串拼接
    src = "data:image/{ext};base64,{data}".format(ext=ext, data=data)
    return src


if __name__ == '__main__':
    # 下载百度首页logo保存到本地 baidu.png
    # https://www.baidu.com/img/bd_logo1.png
    src = "data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAIIAAAAwCAIAAABSYzXUAAAP90lEQVR42u1cB1cbVxbOn9rdsxtv826yyXqTtdclDokT2wnBMdiOQVRJNGGa6CWAKKJXA6YY0U0xvYNEFwIhJCQk1HvxXvKILIaZQcKBTbJ+5505o/fuDKP7zb3fd9+T/c6rn1+zOswmuxaOr/5v2js/n0exv7JJzEtz2qZRdemIugT6jLZhx7Tw/4DHOz+fCAAAJjTV26ZZtVUC0aC1yQCDSU3ttLbe4jC8heE84mBW+2xe13Lc3VaHiafvgLCwOaxvYTjbht568DhRoExp6yBK3sJwtg3SDiBxzP02h0LjMFngVGxeBJzewnC2rACcDEyAPoLfLT0zhoRaXQALdX10ha61f1JUTBQub2H4CRqwMYgiOB6QxI4cnK6PLLd0TdvWxRAN9k2p5SVXn1ynCc03js2/heHsosEEMEA0gN/1tGJTSZdDZ8TY6GyKNU6RLrjQzJn4dcKgV+v+531CXbO9M6ajl+gqX+iVmuMGQvX8uLpKv7R1YNM88uZ/0fID5fyMYOgs5/zP+8BM7U5O4R6V3VXWhmvwcrNyYLYOTqayG7SU/PHvG97wL/Ln135h0ZDk54362UWDepYHVCyeHcCd3VEvjqnLlWop+qirH9TFVeMGzS84Gk60SHnkg/rZPYQxn6MqbAC9tG/dxkwprSLAAASrc8RhMAOHWyc9fp2/jL3i2ufWp0iMYRZj/yuHARQqcK91bmPLNAVIbBhHnIsZm8ZxGIGj45XD9RL184FpelTns4zKPH9W4q2cuE9zEz7LT7rdWhM/2lclE/PdgSGrgUnyVDCLC8P18Dhnr+0dJP9qTstfAAw23ha83a/sdjgH1/P0HWhdDzpXxwFIXI0NOlVfGyuHcSPz24vZUVezn9zA7TUFQaJNLjkMd+OvGc34S1UwDrMnwnArJmlfo/2VwGCq7jMWtmMKOtyFbsHqZEHKXeTozEfvZwVdIoIBenHGPSIY4spp6OTFdAfuI8E4xhIXBujZja1nC4PDYT8fGAxpjVCsnWjGnep09XJz7CNuUrpaKUXPCUfVvmR9ceTF81xIU2AAKYsIhv7ZbnTCKAnB/VswjrEkggH65q70DGHYk01t8Ovl8rnkh96uMOxs8DllRbm0wDT/+xkUv/LEmGFOi1Gvw72JRqmYGuhoq8gpjKOwGI9YjO/qWYlTA+1m0+sCDYgB8hL5U4J/nQDUscMUe9vW4UWot/HrQYtpaqhxcbaXCAazxeTMObv7YowZjLhmLSIYUmufoZOIooozhMFk2pfujq6tVsT6XI3/9ibT77bdbul9WuUMDtfOCg9Wyo68FEaD7sWzstxIv5wI3+OdnRC8tjB5yM8BLPumlOQR9+WivITPEQacp0mOH1jELpTBhQ5PdKerQ1nN6ei8YaAKYwYjaCqnKQVzlatn5WqNVzQTnU8sr501NziSHtxJuO8V63OtJpsCJ/ARFwn2k3DkIGgqhaw8NRwXAGcvYYYe3F2hOYBhT03yBPXFNIRBY1mk80+gC+F4Ohh4gjk4+SLm3wHfY5Mt5ft7yGxhY4YEBjiv6ulH5w/T8+wOx/lQ9DcQEIl+XvWFwVMjubviYaNBLpeIIUE5keCODh2oHfU+uBj5GqKhr6lia5Vrsx1s2sBRxF/ufsqGqfbqfHe8yV8aRRiAHgWZ9PrteDMYxO2tdx9euOH7mxt+v31ZkeVEd0XIQzbfZX51/CqMZ41ms3diBvrY9HL0nJRSRoDfzsa61aoHwgDa2Ns75NXmwhxk0MpmAVXW5cQhDEqTqfJdEe49xZtrC2P97ngTpCeCYXbsiCZ5Exi2asrnI0LYpYwvGB99Tv9HLOWyoKIYIVH0PBvZ1PSWnAgDtM6JafTxTlyq1mA4DxiG25pxpRRg42QIIGSEQXFiiE6tdKt2I+YGuXQTYQA6FcWTs52aGz6n/WOOGqAXCUWyrUMqjrk8TfVXjI/Y7bZvmJ+iQZh1BwZojzPz0Qi7rctgNewbFDqL7gxhUOxK8F1ptyODdIpvUXwggmFrleemd0iU0sTgUwQDyFCsHBpdIlJKJDAAGdx48LudH98neuFj5OKWEuZCVNjgVCf6GF7oj5vKcD07zxdcC4/9MCTsr5THDxv9Azu+g546zOwT9F6lPznX8g0ZJPjeQhg0F2d4UDcw6yw9M7hToIsQDMAQmClzw5Axn+MpDF6hf7vx4Lc242H2aB9rRi5OKKcDDBGJd9FHGHcfhh2N6EpCwIXHDz4IDg0tzIdo2FYLu/kd0X10GPw3Neq8YYjxuYFgQGLU3Sq6rMdU0oU7xU7zRjC4kvOhIM5qNreMegrDJ49+7xX819dljV51O+4qjMNxtCr35qM/oHMYdxMG8Di1OzhrMO/Gj+Pcjc3DF8VmuhhIefexHyBxrjBEf30FwWDQecCc1pl1/ZOqVz9qFdeWE/cpggGbBnVGSGXk1cbxBoQM0uhW1CXXwbS6WOTloIyvYfaL6I9SamOI9BUGBnB0TH9k0XS+3WEHYkDjAdkFrhT9t8BAiAknW+A2ELs/JQxRX32EYPBshVWl0wUW2NbFbsJgtVplbSPq8BJc5EgakDPIU8yS9fjSkNPRQBuf0d4f5Q26CUP9Ym38YAxyMcgkEEtoCuST0xho40/+j+q41UQA9AnWHnPq3xQGeBFUFg3z4dfQI+/+Kyv8HsDgFFHuLyvhZhgW8wsEg9GgtdvtQ5NTzLz8sMRk1OF8YHzCbHZXLHkFX7zp/y4GBlBH95I/Q46+6X/hTth79qMPTwQDcEBwp/+i7PU6LpQOaAqKCSgpnMYfh0UAaUt12Njl7+9F93EC2hs61pc8g8Fst2zohL17o5XbLenrJdHLWWG8ZOgBPpehU+98QAu+Bj2ij8FczS/crOPs9s+oFuXmE5TrwW8vwksdhiNLqlqjpraEmsE4WM0eG2pNLWDHZef2Do9yW/sEYay15TU4T8hhARjCHbE7MICXgRiOb+CUtOchR3uFXEyJ/pKk6HOFoXOdEzsQjXm1fVNz0CwU2K7GzJexbastrsZDQv79lpqS2TGT1eoBN8Q9uFMubKItpoLTU9fZ1dutXdKXU0ouoCI0iBN/iIZo76sZ9G/S6N7FrKhe6Uir5EWeoDpyKQMuSV4rBHtCPKw2fWQ5iJ89taxrti37eUrc04iIyiB68k1qwLs0ygUa7YOMpxnbUqFDowed6gwdCIXa1rbwlPSldT7ajZgbbyP6IpBzIC8dh2F1e+mwpKB/wKH7uglD9lhG41I9xniUt4xmvaKZMqXKady60pQ+kvx6a29X5NNcBenIA4pOeHA39N51is+V4q36CeW83mYgFKz3bzmXjKCWXudOW8wmiHGxUfZc1JPSl0ytoyTlBHDXcZa1hYNDBXkHrs/vzOrndq+JlwESkYSfxrhG++7PUUEXmalfRlRQCstiN5KLMHHT2vMiMi1toLsqP+l2P6eAEAbg54h/kmxnavlrs6GP3YQhtIvCleL8biqiqAKzBAsdchdkMJTuJFr1o7anXfxlD5QSvO+BPleo334C77s7iauxMIVkOQ8CJTrUK3opE4A5ss0y3xlVFVJdwhQkFGB+pJSUHBxFeS8r5jqkprywa6wn3uEFvi/mOtBX0moUUFJAcccI+jDS/+9gs8obwucws+kAhshLJDBAaQ0wgOWJMPyHHgPpXqLFSYYCifT4ngQQA9irjAfJIGmomzU55IFgNdpMkFIifT9zpWiTxa412HRGu9FsN1scFhsU0Q4nDCaDvrUsiwSJqixGs6QH0pqTCTlTzYDB0jb3IOE8qYJqzrlSBKmGlpTaUpuazbieRfkw8/7FLPrllMiP6ZQLsdT3XXeB0qOvUh/+JYn+MdFGtHlfgfQoCQxgAzDA8WQYaAxwK7A07n0y61swMIAlsl/ek0I6kh4T9GQw7FvUkNYh6bvCMLOuY3dIMZ165yvUy3tklb17xfUTmWl5SRHU+CDfOIpPfJBfahQtNz2rorq9bUjUMiOC23bOSQYW1DUD/ZGVIe2TS+Mr2qlV7fz8npzZoA1h71QM8ocFGQUVxaX1kmcTE0G03IeX0uhX0qKuQ0+OuAyEEU/7ZwbjembMIRKpcd6ZeckkLj6AgfETwUAcDQd+02hvxSThRkP22AB7etSz8g2iIXwxvUN6REcbLXal1qrQWPdUFqnSIlGYd+TmbZl5S2oSSEx8sXFtx7iybVgSGnib+gWBfo6vA+TAxRMr2rEl7fCiKp/bEcsr7JtTcia2oqrCynpfdEwqOeP7rWP7LSOK5qG98fJJUWzDemgeqNLNEJaIUTfCGi57vpXJbmSmxMZGejNCP4kMukQL/GNMxO2SgviFyQ6NSiZTKMBeLJW57+JT2JzIDajV9g66wuDkBigRRrYFHlfRwA2ARKmw8UTR6U5b122BdgKZi7gBRFFmK9NOUGT0DY8kZOdh1lAhAVptDrPVASkxrz2reawJEqNzNru0vPvlMBE3gIv1wk2Sx8PlBqKGq5SIGlJKoE29myqhXDjNYobIsAslAkhVAINIKZFW6gdKCQqITH4p5CKQW7umw+cADEAUEV1YWFPX3N1DcueR5cHUpiOrZh39g3mV1UT24GLQQiQ3xFVKRO143UDSUN0g1+sABjnevv077r/IrnVDraitWzYMpRmqG4BFUAfMYISnWevbG4O6IX+zlqhugOoM5OmOYpvoL8Zkfj/DWyR5JKlKAneA+zhHFpZXItMIF3fnI0KUc2Q/AVHx5sHGTYccr6KJ2qp8BVXRbxQNR7Lnj1U0QAJgOKtoTAfXY6ro45lHqdsHJ8IRv56zWiHRbwiFJA9z/A6b2yK4imh5Yy0vY+fozhWmSTrbVrNS3PeG65oS4cKl3Zo8lOBcUzolN7iTc5yhgLrVvX8rSB4NKo0GHCrfV3oUDfsqNVwFR/zs2lzPZ+eR3FBQUSxsqPHgpXRZYSWyqZovj+6jO6E6jVI660bCDeQOJeIG8qsU4yPcGBrJDXnxUXvDgx59BbTfUDrLBkiOgwTjMLuleq0LTlM3nHUjUUruREN+ZxaUfu7DgIQQkR61ajQwqxNsePotdjQiiInIXmo3v0Og5LvuvkGHc4y9x1X0WTdI64yasKn1sVNww5xgGmpvhUbuOkjODQ6rdSEqTD6Kv9qhmBoHfnZYT/Ovr4EA+gS9IGGBtF33onFpQ6JV+z2v9WxN6awbYADe3N7b8kgpASs8qaVBUsKMkyulA5yqSoGo8aVgfragrOgNvw7mlxmE79ApVljPujnXlNysG9bEy4DB88lnx6fI6wZnZQDZCes+sejEquKnbWi/oXxu3N39hnNoaIW1frgKXvPXVfToWEIOCxMETWNPwRLscRmFpIp2fev5hTlYjVRWBOPn/K092307nwbKld2d67rfsLy5Qk1JXNvmC6T8oaV+NAtHIo1LvqbkStRz1ADVwuv/+kG9xDv4ARnpOscZNbvD0buxAsXEfwELpcykEJmLBQAAAABJRU5ErkJggg=="

    # 解码测试
    print(decode_image(src))

