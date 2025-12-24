"""
高校二手商品交易数据集生成脚本
Campus Second-hand Goods Transaction Dataset Generator

本脚本用于生成模拟的高校二手商品交易数据，包括：
- 商品信息
- 交易记录
- 用户信息
- 商品评价
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# 设置随机种子以保证可复现性
np.random.seed(42)
random.seed(42)

# 配置参数
NUM_USERS = 3000  # 用户数量
NUM_PRODUCTS = 8000  # 商品数量
NUM_TRANSACTIONS = 12000  # 交易记录数量
NUM_REVIEWS = 6000  # 评价数量

# 基础数据
UNIVERSITIES = [
    '北京大学', '清华大学', '复旦大学', '上海交通大学', '浙江大学',
    '南京大学', '武汉大学', '华中科技大学', '中山大学', '四川大学',
    '西安交通大学', '哈尔滨工业大学', '同济大学', '东南大学', '天津大学'
]

CATEGORIES = {
    '电子产品': ['手机', '平板电脑', '笔记本电脑', '台式机', '耳机', '音箱', '移动电源', '智能手表', '键盘鼠标', '显示器'],
    '图书教材': ['教材', '考研资料', '英语学习', '专业书籍', '小说', '工具书', '课外读物'],
    '生活用品': ['电吹风', '台灯', '床上用品', '收纳箱', '衣架', '洗漱用品', '小家电'],
    '运动器材': ['自行车', '篮球', '羽毛球拍', '跑步机', '哑铃', '瑜伽垫', '滑板'],
    '服饰鞋包': ['外套', '鞋子', '背包', '帽子', '围巾', 'T恤', '裤子'],
    '乐器': ['吉他', '尤克里里', '电子琴', '口琴', '架子鼓'],
    '家具': ['书桌', '椅子', '书架', '衣柜', '床垫', '小沙发']
}

BRANDS = {
    '手机': ['Apple', '华为', '小米', 'OPPO', 'vivo', '三星', '一加', '魅族'],
    '笔记本电脑': ['Apple', '联想', '华硕', '戴尔', '惠普', '小米', '华为', '微软'],
    '平板电脑': ['Apple', '华为', '小米', '三星', '联想'],
    '耳机': ['Apple', 'Sony', 'Bose', '森海塞尔', 'Beats', '漫步者', '小米'],
    '自行车': ['捷安特', '美利达', '凤凰', '永久', '迪卡侬'],
    '吉他': ['雅马哈', 'Fender', 'Martin', '卡马', '雅依利', '考特'],
}

CONDITIONS = ['全新', '99新', '95新', '9成新', '8成新', '7成新', '6成新']
CONDITION_SCORES = {'全新': 10, '99新': 9.5, '95新': 9, '9成新': 8, '8成新': 7, '7成新': 6, '6成新': 5}

TRANSACTION_STATUS = ['已完成', '已完成', '已完成', '已完成', '已完成', '已取消', '退款中']

# 生成时间范围：2020-2024学年
START_DATE = datetime(2020, 9, 1)
END_DATE = datetime(2024, 6, 30)


def generate_realistic_price(category, subcategory, brand, condition, original_price):
    """根据商品属性生成合理的二手价格"""
    base_price = original_price
    
    # 成色折扣
    condition_discount = {
        '全新': 0.95,
        '99新': 0.85,
        '95新': 0.75,
        '9成新': 0.65,
        '8成新': 0.50,
        '7成新': 0.40,
        '6成新': 0.30
    }
    
    price = base_price * condition_discount.get(condition, 0.5)
    
    # 品牌溢价
    premium_brands = ['Apple', 'Sony', 'Bose', '森海塞尔', 'Fender', 'Martin']
    if brand in premium_brands:
        price *= random.uniform(1.1, 1.3)
    
    # 添加随机波动
    price *= random.uniform(0.9, 1.1)
    
    # 取整到10元
    price = round(price / 10) * 10
    
    return max(price, 10)  # 最低10元


def random_date(start, end):
    """生成随机日期"""
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)


def generate_users():
    """生成用户数据"""
    print("正在生成用户数据...")
    
    users = []
    for i in range(NUM_USERS):
        user_id = f"U{str(i+1).zfill(6)}"
        username = f"user_{random.randint(10000, 99999)}"
        university = random.choice(UNIVERSITIES)
        
        # 入学年份
        enrollment_year = random.choice([2018, 2019, 2020, 2021, 2022, 2023])
        grade = ['大一', '大二', '大三', '大四', '研一', '研二', '研三'][
            min(2024 - enrollment_year, 6)
        ]
        
        register_date = random_date(
            datetime(enrollment_year, 9, 1),
            datetime(2024, 6, 30)
        )
        
        # 信用评分 (60-100)
        credit_score = random.randint(60, 100)
        
        users.append({
            'user_id': user_id,
            'username': username,
            'university': university,
            'enrollment_year': enrollment_year,
            'grade': grade,
            'register_date': register_date.strftime('%Y-%m-%d'),
            'credit_score': credit_score,
            'total_transactions': 0,  # 后续更新
            'total_sales': 0  # 后续更新
        })
    
    return pd.DataFrame(users)


def generate_products(users_df):
    """生成商品数据"""
    print("正在生成商品数据...")
    
    products = []
    
    for i in range(NUM_PRODUCTS):
        product_id = f"P{str(i+1).zfill(6)}"
        
        # 选择分类和子分类
        category = random.choice(list(CATEGORIES.keys()))
        subcategory = random.choice(CATEGORIES[category])
        
        # 品牌
        if subcategory in BRANDS:
            brand = random.choice(BRANDS[subcategory])
        else:
            brand = random.choice(['无品牌', '杂牌', '其他'])
        
        # 成色
        condition = random.choice(CONDITIONS)
        
        # 原价（根据商品类型）
        price_ranges = {
            '手机': (2000, 8000),
            '笔记本电脑': (3000, 15000),
            '平板电脑': (1500, 6000),
            '台式机': (2000, 10000),
            '耳机': (100, 2000),
            '自行车': (300, 2000),
            '吉他': (500, 5000),
            '教材': (20, 150),
            '电吹风': (50, 300),
            '台灯': (30, 200),
            '书桌': (200, 800),
        }
        
        original_price = random.randint(
            *price_ranges.get(subcategory, (50, 500))
        )
        
        # 二手价格
        price = generate_realistic_price(
            category, subcategory, brand, condition, original_price
        )
        
        # 使用时长（月）
        usage_months = random.randint(
            1, 48 if category != '图书教材' else 12
        )
        
        # 卖家
        seller_id = random.choice(users_df['user_id'].values)
        
        # 发布日期
        publish_date = random_date(START_DATE, END_DATE)
        
        # 商品状态
        status = random.choice(
            ['在售', '在售', '在售', '已售出', '已售出', '已售出', '已售出', '已下架']
        )
        
        # 浏览量
        views = random.randint(10, 500)
        
        # 收藏量
        favorites = random.randint(0, views // 3)
        
        products.append({
            'product_id': product_id,
            'title': f"{brand} {subcategory} {condition}",
            'category': category,
            'subcategory': subcategory,
            'brand': brand,
            'condition': condition,
            'condition_score': CONDITION_SCORES[condition],
            'original_price': original_price,
            'selling_price': price,
            'usage_months': usage_months,
            'seller_id': seller_id,
            'publish_date': publish_date.strftime('%Y-%m-%d'),
            'status': status,
            'views': views,
            'favorites': favorites,
            'description': f"{condition}{subcategory}，使用{usage_months}个月，保养良好"
        })
    
    return pd.DataFrame(products)


def generate_transactions(products_df, users_df):
    """生成交易记录"""
    print("正在生成交易记录...")
    
    transactions = []
    
    # 选择已售出的商品
    sold_products = products_df[
        products_df['status'] == '已售出'
    ].sample(n=min(NUM_TRANSACTIONS, len(products_df[products_df['status'] == '已售出'])))
    
    for idx, product in sold_products.iterrows():
        transaction_id = f"T{str(len(transactions)+1).zfill(6)}"
        
        # 买家（不能是卖家本人）
        buyer_id = random.choice(
            users_df[users_df['user_id'] != product['seller_id']]['user_id'].values
        )
        
        # 交易日期（在发布日期之后）
        publish_date = datetime.strptime(product['publish_date'], '%Y-%m-%d')
        transaction_date = random_date(
            publish_date,
            min(END_DATE, publish_date + timedelta(days=60))
        )
        
        # 成交价（可能会议价）
        final_price = product['selling_price'] * random.uniform(0.9, 1.0)
        final_price = round(final_price / 10) * 10
        
        # 交易状态
        status = random.choice(TRANSACTION_STATUS)
        
        # 交易地点
        location = random.choice([
            '校门口', '图书馆门口', '食堂', '宿舍楼下', '体育馆',
            '快递站', '教学楼', '线上交易'
        ])
        
        transactions.append({
            'transaction_id': transaction_id,
            'product_id': product['product_id'],
            'seller_id': product['seller_id'],
            'buyer_id': buyer_id,
            'transaction_date': transaction_date.strftime('%Y-%m-%d %H:%M:%S'),
            'selling_price': product['selling_price'],
            'final_price': final_price,
            'discount_rate': round((product['selling_price'] - final_price) / product['selling_price'] * 100, 2),
            'status': status,
            'location': location,
            'payment_method': random.choice(['微信', '支付宝', '现金', '银行卡'])
        })
    
    return pd.DataFrame(transactions)


def generate_reviews(transactions_df, users_df):
    """生成评价数据"""
    print("正在生成评价数据...")
    
    reviews = []
    
    # 从已完成的交易中随机选择
    completed_transactions = transactions_df[
        transactions_df['status'] == '已完成'
    ].sample(n=min(NUM_REVIEWS, len(transactions_df[transactions_df['status'] == '已完成'])))
    
    # 5星好评（60%）
    positive_5_comments = [
        '商品和描述一致，卖家很诚信！',
        '东西不错，性价比超高，推荐购买',
        '成色很好，物超所值，非常满意',
        '交易顺利，卖家人很好，沟通也很愉快',
        '质量不错，值得购买，下次还来',
        '物品完好无损，包装也很仔细',
        '卖家很耐心解答问题，商品质量也好',
        '价格公道，东西实在，良心卖家',
        '收到货很惊喜，比想象中好很多',
        '宝贝收到了，和图片一模一样',
        '超级满意，卖家态度特别好',
        '非常棒的购物体验，五星好评',
        '东西很新，几乎没怎么用过',
        '物流很快，商品质量也很好',
        '卖家很靠谱，约的时间地点都很准时',
        '物品保养得很好，看得出很爱惜',
        '性价比真的很高，捡到宝了',
        '比去某宝买便宜太多了，赚了',
        '学长人很好，还送了配件',
        '东西很实用，正好需要',
        '卖家很专业，讲解得很详细',
        '物品成色比描述的还好',
        '完美的交易体验，感谢卖家',
        '同校交易就是方便，当面验货放心',
        '学姐人超好，还教我怎么使用',
        '东西保养得非常好，点赞',
        '价格实惠，质量过硬',
        '卖家很负责，交易很顺利',
        '物品功能完好，非常满意',
        '比预期好太多了，强烈推荐',
        '良心价格，良心卖家',
        '超值，下次有需要还来',
        '卖家态度好，东西也好',
        '很满意的一次购物',
        '物品如描述，好评',
        '收到了，很好用，感谢',
        '完美，没有任何问题',
        '非常好，推荐给室友了',
        '东西很棒，卖家人也很好',
        '满意满意，五星好评',
        '太棒了，超出预期',
        '买到就是赚到，强推',
        '卖家诚信，商品优质',
        '非常愉快的交易',
        '物美价廉，值得信赖',
    ]
    
    # 4星好评（25%）
    positive_4_comments = [
        '整体不错，有点小瑕疵但不影响使用',
        '东西还可以，符合预期',
        '性价比可以，物有所值',
        '卖家态度好，商品也还行',
        '还不错，就是价格稍微有点高',
        '质量可以，就是有点使用痕迹',
        '总体满意，小细节还有改进空间',
        '物品基本符合描述，好评',
        '不错的购物体验，就是约见面有点麻烦',
        '东西还行，卖家也挺好说话的',
        '可以用，性价比还算可以',
        '基本满意，就是外观有点旧',
        '功能正常，有些使用痕迹',
        '还行，符合二手的标准',
        '卖家挺实在的，东西也还可以',
        '物品能用，价格也合理',
        '整体OK，有点小问题但能接受',
        '还可以，就是没有配件了',
        '不错，就是有点旧',
        '可以，基本满足需求',
        '挺好的，虽然不是全新但很值',
        '满意，就是包装简单了点',
        '商品质量不错，略有瑕疵',
        '算是比较满意的',
        '还可以，下次可能还会来',
    ]
    
    # 3星中评（10%）
    neutral_3_comments = [
        '还行吧，凑合用',
        '和预期差不多，一般般',
        '能用，但谈不上多好',
        '商品还可以，没有惊喜',
        '一般般，符合这个价位',
        '普通，不好不坏',
        '和描述有点出入，但还能接受',
        '成色比预期的要旧一些',
        '凑合着用吧，毕竟是二手的',
        '没啥特别的，就是便宜',
        '东西一般，但价格还行',
        '有点失望，不过也能用',
        '不是特别满意，但也不算太差',
        '中规中矩，没什么可说的',
        '和图片有些差距，还能用',
        '说不上好也说不上坏',
        '价格合适，东西一般',
        '勉强及格吧',
        '有点旧了，但还能用',
        '凑合，毕竟便宜',
    ]
    
    # 2星差评（3%）
    negative_2_comments = [
        '成色比描述差很多',
        '有些小瑕疵没有提前说明',
        '价格有点贵，不太划算',
        '和图片差距比较大',
        '东西有点旧，有点失望',
        '卖家态度一般，东西也就那样',
        '有点上当的感觉',
        '不太满意，有点后悔买了',
        '实物和描述不太一致',
        '质量比预期差',
        '有隐藏的问题没说',
        '感觉不值这个价',
        '比较失望',
        '不推荐购买',
        '有点坑',
    ]
    
    # 1星极差评（2%）
    negative_1_comments = [
        '严重不符，强烈不推荐',
        '完全和描述不一样，太坑了',
        '东西有很大问题，卖家态度还不好',
        '质量太差了，根本不能用',
        '感觉被骗了，差评',
        '千万别买，血的教训',
        '简直就是骗人的',
        '太失望了，浪费钱',
        '完全不能用，要求退款',
        '极度不推荐，垃圾',
    ]
    
    for idx, transaction in completed_transactions.iterrows():
        review_id = f"R{str(len(reviews)+1).zfill(6)}"
        
        # 评分（1-5分）
        rating = random.choices(
            [5, 4, 3, 2, 1],
            weights=[0.6, 0.25, 0.1, 0.03, 0.02]
        )[0]
        
        # 根据评分选择对应的评论内容
        if rating == 5:
            comment = random.choice(positive_5_comments)
        elif rating == 4:
            comment = random.choice(positive_4_comments)
        elif rating == 3:
            comment = random.choice(neutral_3_comments)
        elif rating == 2:
            comment = random.choice(negative_2_comments)
        else:
            comment = random.choice(negative_1_comments)
        
        # 评价时间（交易后1-7天）
        transaction_date = datetime.strptime(
            transaction['transaction_date'],
            '%Y-%m-%d %H:%M:%S'
        )
        review_date = transaction_date + timedelta(days=random.randint(1, 7))
        
        reviews.append({
            'review_id': review_id,
            'transaction_id': transaction['transaction_id'],
            'product_id': transaction['product_id'],
            'reviewer_id': transaction['buyer_id'],
            'rating': rating,
            'comment': comment,
            'review_date': review_date.strftime('%Y-%m-%d %H:%M:%S'),
            'is_anonymous': random.choice([0, 0, 0, 1])  # 75%实名
        })
    
    return pd.DataFrame(reviews)


def main():
    """主函数"""
    print("=" * 50)
    print("高校二手商品交易数据集生成器")
    print("=" * 50)
    print()
    
    # 创建输出目录
    os.makedirs('data', exist_ok=True)
    
    # 生成各类数据
    users_df = generate_users()
    products_df = generate_products(users_df)
    transactions_df = generate_transactions(products_df, users_df)
    reviews_df = generate_reviews(transactions_df, users_df)
    
    # 保存数据
    print("\n正在保存数据...")
    users_df.to_csv('data/users.csv', index=False, encoding='utf-8-sig')
    products_df.to_csv('data/products.csv', index=False, encoding='utf-8-sig')
    transactions_df.to_csv('data/transactions.csv', index=False, encoding='utf-8-sig')
    reviews_df.to_csv('data/reviews.csv', index=False, encoding='utf-8-sig')
    
    # 生成数据统计
    print("\n" + "=" * 50)
    print("数据生成完成！")
    print("=" * 50)
    print(f"\n数据统计：")
    print(f"  用户数量: {len(users_df):,}")
    print(f"  商品数量: {len(products_df):,}")
    print(f"  交易记录: {len(transactions_df):,}")
    print(f"  评价数量: {len(reviews_df):,}")
    print(f"\n数据文件已保存到 'data' 目录")
    print(f"  - users.csv (用户信息)")
    print(f"  - products.csv (商品信息)")
    print(f"  - transactions.csv (交易记录)")
    print(f"  - reviews.csv (评价信息)")
    
    # 显示数据预览
    print("\n" + "=" * 50)
    print("数据预览")
    print("=" * 50)
    print("\n商品数据前5条：")
    print(products_df.head())
    
    print("\n交易数据前5条：")
    print(transactions_df.head())


if __name__ == '__main__':
    main()

