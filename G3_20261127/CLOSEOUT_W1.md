# W1 CLOSEOUT（G3，2026-11-27）

- candidate：`W1-G3-PCNF-r2`；source manifest `f00b4ee93611e738e409d40758aa320b0bfec3ef0a01fea04dbf5bcb9f1566dc`
- pack tree `22fa47302ebcbb185b98b2c5d0a2bfa90b68becf31cd9f393be4d2ebdd669004`；case set `9e5c6a83b719c400c8d38e82156f494de8d3da65e9ccf32cef3c6c2b8dfd8262`
- raw：`G3_20261127/runs/w1/`

## 13 原案

**12 PASS＋1 DEFERRED**（`W1-HERMES-01`：真 falsifier `REQUIRED_CHILD_MISSING`；Hermes host 未綁，POS 不宣）。

## 67 ECP 逐列（measured）

`runs/w1/raw/ECP67_MEASURED.json`：**61 PASS／1 PARTIAL／3 DEFERRED_HOST／2 REASONED_NA**（合計 67）。

- 每列有 `evidence` 指標與 observed 說明；不再以 prior disposition 冒本輪。
- 唯一 PARTIAL：`OPS-POST-03`（Checker／Consumer 為分離程序但同一 OS principal，不能宣 independent）。
- DEFERRED_HOST：`OPS-CON-01`（ChatGPT）、`OPS-CON-03`／`OPS-POST-04`（Hermes 三 child）。
- REASONED_NA：`OPS-REC-01/02`（未 install／未 register，無 recovery 對象）。

## 第二工作包與產品能力

- `runs/w1/raw/SECOND_PACK.json`：同一 TPM/Guide/BodyResolver 對 **W1（13 案）** 與 **W2（12 案）** 兩包建五視圖；`verdict=PASS`、`distinct=true`；W2 視圖 PI/PD/DEV/OPS/TQAEP＝12/8/7/7/8。
- TPM 三 SPEC／四契約：`tpm_contracts_nf.build_contracts` + `review`（G3 profile 新增；115 tests 仍 OK）。
- Guide：same→`PARK_NO_DELTA`、delta→`NEW_MATERIAL_EVIDENCE`、缺期→`DELTA_UNVERIFIED`。
- API/BodyResolver：84 clauses／167 NEG／27 exceptions。
- Host：CODEX 七階段；21 格 observed 7/21。
- 115 tests OK（含 gate／receiver／BodyResolver／TPM／Guide）。

## 判定

**`W1_SCOPED_PARTIAL`**：61/67 本輪 observed、2 NA、3 host-deferred、1 結構性 PARTIAL。除 independent principal 與外部 Host 外，W1 產品能力與 13 案已閉合。

## 未閉項

- `W1-HERMES-01` 與 Hermes 三 child；ChatGPT／GPT WORK。
- `OPS-POST-03` 需另一 principal（不可自簽）。
