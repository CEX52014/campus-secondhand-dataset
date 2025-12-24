# 数据集使用指南

## 快速开始

### 1. 克隆或下载数据集

```bash
git clone https://github.com/YOUR_USERNAME/campus-secondhand-dataset.git
cd campus-secondhand-dataset
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 使用数据集

#### Python示例

```python
import pandas as pd

# 读取数据
users = pd.read_csv('data/users.csv')
products = pd.read_csv('data/products.csv')
transactions = pd.read_csv('data/transactions.csv')
reviews = pd.read_csv('data/reviews.csv')

# 数据探索
print("商品类别分布：")
print(products['category'].value_counts())

print("\n平均成交价：")
print(f"¥{transactions['final_price'].mean():.2f}")

print("\n评价评分分布：")
print(reviews['rating'].value_counts())
```

## 数据集特点

### 1. 真实性
- 基于真实高校二手交易场景设计
- 符合学生消费行为特征
- 价格分布合理

### 2. 完整性
- 包含用户、商品、交易、评价四个维度
- 数据关联关系完整
- 字段齐全

### 3. 多样性
- 7大商品类别，30+子类别
- 114种不同的评价文本
- 15所高校数据

### 4. 可用性
- CSV格式，易于读取
- 字段命名规范
- 文档详细

## 应用场景示例

### 场景1：价格预测模型

```python
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
import pandas as pd

# 读取商品数据
products = pd.read_csv('data/products.csv')

# 特征工程
features = ['condition_score', 'original_price', 'usage_months', 'views', 'favorites']
X = products[features]
y = products['selling_price']

# 训练模型
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = XGBRegressor()
model.fit(X_train, y_train)

# 预测
print(f"模型R²分数: {model.score(X_test, y_test):.3f}")
```

### 场景2：用户行为分析

```python
# 分析用户购买偏好
user_purchases = transactions.merge(products, on='product_id')
category_preference = user_purchases.groupby(['buyer_id', 'category']).size()
print("用户购买偏好TOP5：")
print(category_preference.nlargest(5))
```

### 场景3：情感分析

```python
# 评价情感分析
from sklearn.feature_extraction.text import TfidfVectorizer

reviews_df = pd.read_csv('data/reviews.csv')
positive_reviews = reviews_df[reviews_df['rating'] >= 4]['comment']
negative_reviews = reviews_df[reviews_df['rating'] <= 2]['comment']

print(f"正面评价数量: {len(positive_reviews)}")
print(f"负面评价数量: {len(negative_reviews)}")
```

### 场景4：推荐系统

```python
# 基于协同过滤的商品推荐
from sklearn.metrics.pairwise import cosine_similarity

# 构建用户-商品矩阵
user_item_matrix = transactions.pivot_table(
    index='buyer_id', 
    columns='product_id', 
    values='final_price',
    fill_value=0
)

# 计算相似度
user_similarity = cosine_similarity(user_item_matrix)
print("用户相似度矩阵构建完成")
```

## 数据验证

运行验证脚本检查数据质量：

```bash
python verify_data.py
```

## 重新生成数据

如果需要生成新的数据集（不同的随机种子）：

```bash
python generate_dataset.py
```

## 常见问题

### Q1: 数据是真实的吗？
A: 本数据集是基于真实场景模拟生成的，数据分布和规律参考了真实的高校二手交易平台。

### Q2: 可以用于商业项目吗？
A: 不可以。本数据集采用CC BY-NC-SA 4.0许可，仅限非商业使用。

### Q3: 数据中有缺失值吗？
A: 核心字段无缺失值，缺失率<2%。

### Q4: 如何引用这个数据集？
A: 请参考README.md中的引用格式。

## 技术支持

- GitHub Issues: [提交问题](https://github.com/YOUR_USERNAME/campus-secondhand-dataset/issues)
- Email: data-team@university.edu.cn

## 更新日志

- **v1.0.0** (2024-06-30): 初始版本发布

---

**祝使用愉快！如有问题欢迎反馈。**

