"""种子数据脚本（可重复执行：先清空再插入）

用法: python scripts/seed.py
"""
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from app.db import SessionLocal, init_db  # noqa: E402
from app.models import Category, Script, Store, StoreRule  # noqa: E402


STORES = [
    {"name": "云栖数码官方旗舰店", "platform": "淘宝", "notes": "主力店铺，主打蓝牙耳机与智能穿戴"},
    {"name": "云栖数码京东自营店", "platform": "京东", "notes": "京东自营供货，物流时效要求高"},
    {"name": "云栖数码拼多多店", "platform": "拼多多", "notes": "低价引流款，售后纠缠较多"},
]

CATEGORIES = [
    {"name": "单产品售前话术", "type": "售前", "sort_order": 1},
    {"name": "售后通用话术", "type": "售后", "sort_order": 2},
    {"name": "产品售后纠缠话术", "type": "售后", "sort_order": 3},
    {"name": "后台申诉话术", "type": "申诉", "sort_order": 4},
    {"name": "产品技术类话术", "type": "技术", "sort_order": 5},
]

# (标题, 内容, 标签, 分类名, 店铺名或 None)
SCRIPTS = [
    # 单产品售前话术
    (
        "新品蓝牙耳机介绍",
        "亲，您好呀~这款XX蓝牙耳机是我们的新品，支持蓝牙5.3连接、主动降噪、续航36小时，现在下单还送收纳盒+保护套哦！有任何问题随时问我~",
        "新品,蓝牙耳机",
        "单产品售前话术",
        "云栖数码官方旗舰店",
    ),
    (
        "智能手环价格咨询",
        "亲，这款智能手环现在活动价199元，支持心率监测、血氧检测、50米防水，7天无理由退换，您可以放心下单~",
        "价格,智能手环",
        "单产品售前话术",
        None,
    ),
    (
        "库存与发货时效确认",
        "亲，这款商品目前现货充足，拍下后48小时内发货，顺丰包邮，预计2-3天到货哦~",
        "发货,时效",
        "单产品售前话术",
        "云栖数码京东自营店",
    ),
    # 售后通用话术
    (
        "物流延迟安抚",
        "亲，非常抱歉给您带来不便！您反馈的物流延迟问题我们已经加急催件了，快递一般会在24小时内更新物流信息，请您耐心等待一下，给您补发一张5元优惠券表示歉意~",
        "物流,安抚",
        "售后通用话术",
        None,
    ),
    (
        "无理由退货引导",
        "亲，支持7天无理由退货哦~您只需在订单页面点击申请售后，选择退货退款，填写退货原因提交即可，我们会在24小时内审核通过~",
        "退货,退款",
        "售后通用话术",
        None,
    ),
    (
        "发票开具说明",
        "亲，本店支持开具电子发票，您下单时备注发票抬头或联系我登记，确认收货后1-3个工作日发送到您的邮箱~",
        "发票",
        "售后通用话术",
        "云栖数码官方旗舰店",
    ),
    # 产品售后纠缠话术
    (
        "质量问题坚持换新",
        "亲，您反馈的商品质量问题我们非常重视。请您提供一下商品故障照片或视频，我们核实后会为您安排换新，来回运费由我们承担，您放心~",
        "质量问题,换新",
        "产品售后纠缠话术",
        None,
    ),
    (
        "仅退款拒绝话术",
        "亲，非常理解您的心情~不过根据平台规则，商品已发货且无质量问题的订单无法支持仅退款哦。我们提供退换货服务，运费我们承担，您看可以吗？",
        "仅退款,纠缠",
        "产品售后纠缠话术",
        "云栖数码拼多多店",
    ),
    (
        "多次催退款安抚",
        "亲，您的退款申请我们已经加急处理啦~平台退款审核一般需要1-3个工作日，我们这边会持续跟进，确保退款尽快到账，请您放心~",
        "退款,催办",
        "产品售后纠缠话术",
        None,
    ),
    # 后台申诉话术
    (
        "差评申诉话术",
        "亲，关于您反馈的这条差评，我们已经与买家沟通核实情况，现将沟通记录和发货凭证整理提交后台申诉，请您同步提供相关凭证支持~",
        "差评,申诉",
        "后台申诉话术",
        None,
    ),
    (
        "平台判罚申诉",
        "亲，针对本次平台判罚，我们已准备完整的申诉材料（包括聊天记录、物流凭证、商品质检报告），将于今日提交后台申诉，后续进度会第一时间同步给您~",
        "判罚,申诉",
        "后台申诉话术",
        "云栖数码官方旗舰店",
    ),
    # 产品技术类话术
    (
        "蓝牙耳机连接不上",
        "亲，蓝牙连不上请按以下步骤排查：1）确认耳机有电并处于配对模式（长按触控区3秒）2）删除手机中旧配对记录重新搜索 3）若仍无法连接，尝试恢复出厂（连续点按5次），如果还有问题随时联系我~",
        "蓝牙,连接,技术",
        "产品技术类话术",
        None,
    ),
    (
        "手环无法同步数据",
        "亲，手环无法同步请先检查：1）手机蓝牙是否开启 2）App是否为最新版本 3）手环电量是否充足，重启App再试；仍不行可以卸载重装App，数据会自动恢复~",
        "手环,同步,技术",
        "产品技术类话术",
        "云栖数码京东自营店",
    ),
]

# (店铺名, 规则类型, 标题, 内容)
RULES = [
    (
        "云栖数码官方旗舰店",
        "退款",
        "旗舰店退款政策",
        "7天无理由退货，质量问题30天内包换；退款审核不超过24小时",
    ),
    (
        "云栖数码官方旗舰店",
        "运费",
        "运费承担规则",
        "质量问题退货运费由店铺承担；非质量问题退货运费买家自理（首重12元）",
    ),
    (
        "云栖数码京东自营店",
        "时效",
        "售后时效承诺",
        "售后响应时效：工作日2小时内回复，退款审核1个工作日内完成",
    ),
    (
        "云栖数码京东自营店",
        "纠纷",
        "纠纷处理原则",
        "涉及赔付纠纷时，优先按京东平台规则执行，赔付金额上限为订单金额的30%",
    ),
    (
        "云栖数码拼多多店",
        "退款",
        "拼多多店退款规则",
        "支持'先用后付'订单即时退款；普通订单退款审核不超过48小时",
    ),
]


def main() -> None:
    init_db()
    db = SessionLocal()
    try:
        # 清空旧数据（保持可重复执行）
        db.query(StoreRule).delete()
        db.query(Script).delete()
        db.query(Category).delete()
        db.query(Store).delete()

        store_by_name = {}
        for item in STORES:
            store = Store(**item)
            db.add(store)
            store_by_name[item["name"]] = store

        category_by_name = {}
        for item in CATEGORIES:
            category = Category(**item)
            db.add(category)
            category_by_name[item["name"]] = category

        db.flush()  # 拿到自增 id

        for title, content, tags, cat_name, store_name in SCRIPTS:
            db.add(
                Script(
                    title=title,
                    content=content,
                    tags=tags,
                    category_id=category_by_name[cat_name].id,
                    store_id=store_by_name[store_name].id if store_name else None,
                )
            )

        for store_name, rule_type, title, content in RULES:
            db.add(
                StoreRule(
                    store_id=store_by_name[store_name].id,
                    rule_type=rule_type,
                    title=title,
                    content=content,
                )
            )

        db.commit()

        n_stores = db.query(Store).count()
        n_cats = db.query(Category).count()
        n_scripts = db.query(Script).count()
        n_rules = db.query(StoreRule).count()
        print(
            f"✅ 种子数据完成：{n_stores} 个店铺、{n_cats} 个分类、"
            f"{n_scripts} 条话术、{n_rules} 条售后规则"
        )
    finally:
        db.close()


if __name__ == "__main__":
    main()
