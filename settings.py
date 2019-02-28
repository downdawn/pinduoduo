# -*- coding: utf-8 -*-

# Scrapy settings for pinduoduo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'pinduoduo'

SPIDER_MODULES = ['pinduoduo.spiders']
NEWSPIDER_MODULE = 'pinduoduo.spiders'


DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
REDIS_URL = "redis://127.0.0.1:6379"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'pinduoduo (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False


# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
#   'Host': 'apiv3.yangkeduo.com',
#   'AccessToken':'WPKHYTN6D5YYNC6FZIVVAH3TXQ2IYHWF5T35UJVBIEDON56NF47A10312a4',
#   'cookie':'api_uid=rBQh5lwt5tIz5kOSFgGsAg==; _nano_fp=XpdYn5daX59JnqTaXC_yIU_LNQ_M7ShVGMFp9Twc; msec=1800000; pdd_user_uin=ZYXPDBINPYLGJO5SOEUSCV6ML4_GEXDA; pdd_user_id=1528432695058; PDDAccessToken=WPKHYTN6D5YYNC6FZIVVAH3TXQ2IYHWF5T35UJVBIEDON56NF47A10312a4; rec_list_personal=rec_list_personal_PukFyh; ab=0; gp=0; rec_list_index=rec_list_index_ZtrfcY; rec_list_catgoods=rec_list_catgoods_NL09Bs; sp=1; ua=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F70.0.3538.110%20Safari%2F537.36; webp=1; rec_list=rec_list_13cfnX; goods_detail_mall=goods_detail_mall_ehF1Wj'
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'pinduoduo.middlewares.PinduoduoSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'pinduoduo.middlewares.ProxyMiddleware': 540,
   'pinduoduo.middlewares.RandomUserAgentMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
   'scrapy.extensions.telnet.RedisSpiderSmartIdleClosedExensions': None,
}
MYEXT_ENABLED=True      # 开启扩展
IDLE_NUMBER=10           # 配置允许的空闲时长，每5秒会增加一次IDLE_NUMBER，直到增加到10，程序才会close

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'pinduoduo.pipelines.MongoPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


MONGO_URI = "localhost"
MONGO_DB = "pinduoduo"

PROXY_URL = 'http://localhost:5555/random'