# NDMF_BUILD_PASS_SHARED

## 目的
次回 NDMF Build Pass を触る時の入口になる、薄い shared note。

## 今の時点で再利用しやすい判断
- local package source を一次ソース優先にする
- NDMF optional dependency は、専用 asmdef 分離をまず検討する
- plugin は薄く、core は NDMF 非依存に寄せる
- build 補正は UI 保存結果より build clone 再列挙を正にする
- ordering は pass 単位に寄せすぎず、まず plugin 単位の弱い順序から始める

## まだ不確実なこと
- NDMF 2.x
- MA 未導入時
- SDK reflection 名依存
- compile 環境依存

## 詳細を見る場所
- 詳細は対象 repo の `Documentation~/notes/NDMF_BUILD_PASS_NOTES.md` を見る

## 次回見る順番
1. 対象 repo の `NDMF_BUILD_PASS_NOTES.md` を確認する
2. local package source と version を確認する
3. optional dependency と asmdef 分離の要否を確認する
4. build clone 再列挙を正にする方針で見る
5. plugin 単位の弱い順序から ordering を確認する
