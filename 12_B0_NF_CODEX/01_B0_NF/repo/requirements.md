# briefcheck Requirements (B0-NF)

SAMPLE-R1｜受權 root 內 UTF-8 Markdown；input 為 root 內相對路徑；核 SHA-256。

A和B各有獨立必要 Child；SAMPLE-R2｜parent PASS 若且唯若 A、B 都存在、已勾選且唯一。

SAMPLE-R3｜stdout 為穩定 UTF-8 JSON：`source_sha256`, `provided`, `missing`, `status`；不回寫來源；exit 0=完整，2=缺項，3=無效/越權。

SAMPLE-R4｜同一 source 執行兩次結果相同；可在受權 output root 作一次可逆寫入並 readback。

NEG｜絕對路徑、`..`、UNC、symlink/junction/reparse escape、非法 UTF-8、hash mismatch、duplicate、ambiguous、malformed 必須 fail closed。
