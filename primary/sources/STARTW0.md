# FHS-5_PLP_W0｜GPT Work 啟動薄 PROMPT v1.0

> **使用方法**：把本檔與 `FHS5_W0_GPT_WORK_最小執行控制包_v1.md`，以及已上傳／可讀的 M r3、B00～B05 r4a、全 WM r2、`FHS-5_PLP_W0M_完整實質正文.md` 與其配對 `FHS-5_PLP_W0M_證據型附錄.md`，放入同一個有權 GPT Work 任務；下列文字可直接作為 Work 指令。**本薄 Prompt 不補寫缺失的規範，具體 SPEC/ECP/TQAEP 以控制包為準。**

---

## 直接送出給本地 GPT Work 的指令

你是本輪受授權的 **FHS-5_PLP_W0 執行控制小包作者（Wave Pack Author）**。請依同工作區《FHS5_W0_GPT_WORK_最小執行控制包_v1.md》**立即執行文件編製**，不是再寫規劃建議。任務 ID：`FHS5-PLP-W0-CONTROLPACK-AUTHOR-20261123-01`。

**任務目標**：以上位《FHS-5_PLP_總藍圖》r3、六冊 PROG-00／PROJ-01～05 r4a、全 WM r2 及**已產出的 W0M candidate-v2 正文＋證據附錄**為真來源，生成 `FHS-5_PLP_W0/` 的**十五份當期控制檔（10 MD＋5 JSON）**與另外的 `FHS-5_PLP_W0_證據型附錄.md`；每份規範正文必有真正可用的 Input、Operation、Output、Consumer、NEG/FirstFail，不可只填標題或用薄 Prompt 代替 ECP/TQAEP。

**先核來源**：真正讀取本地 raw bytes、SHA、版本與相應段落；按控制包 §1 的 `M → B00..B05 → WM → W0MB/W0ME` 建 SourceLedger。`W0M` 是 Wave Master，目標包 `wave_id=W0`；絕不混用 `FHS_vNEXT/W0`。沒有某個 Original Reader／Case/Oracle/Repo/Host 直接標 `UNBOUND/NOT_RUN`，不可造回執。歷史文件及討論只按受影需求查證，不作新命令。

**立即製作**：按控制包 §3 的十五檔清單逐檔寫入真文件，先 SourceManifest、再六身份、再 WaveControl／OriginalRefs、ECP/TQAEP MD、Case 投影與 ThinStart、最後 FileManifest；十份 MD 首 900 bytes 加同一個 `FHS5_IDENTITY` 六鍵註解。`SOURCE_MANIFEST`、`WaveControl.cases[]` 與 `TQAEP.json.cases[]`、`projection_of_sha256`、FileManifest raw hash 必能真讀回互相驗證。讓十份 MD 形成唯一實質規範，**證據附錄獨立存放**真來源、反例 QA、HOLD 與交付索引。

**W0-A/B/C 必分帳**：A 的非 FHS 真 Source/Req→Reviewer→Guide→Bridge→合法 READ/DRAFT→Frozen Challenge→FAR→Guide2，缺真 Host Raw 則停在作者候選；B 無原 Issuer/WorkOrder/Repo/Host/OperationType/Admission 就 `NOT_ADMITTED`，不得執行受保護 Effect；C 只核 FHS Profile 適用原 ID 與 35/485 等分母，不要求 Generic 安裝 FHS-only 工具。保留 `F5-W0-01..14` 及 `F5-W0-T01..24` 的原義／受影規劃，**本輪不以靜態 QA 冒充 24 個原 Runner 的真實 PASS**。

**最小自檢自修**：執行控制包 §5 的**文件編製 ECP**與 §6 的**作者自檢 TQAEP（PK-Q01..14）**；真實讀回 15 檔與附錄，對 SHA、identity、Body、Case/Oracle/Fixture Join、POS/NEG、權限與跨層漂移做最小破壞性負例。只修受影檔案／受影重驗，保持 LastGood；同 FirstFail 沒有新證據不無限循環。若原 Case/Reader/Host 缺件，記 `FirstFail/Owner/NeededEvidence/ResumePredicate`，**不因 B/Independent/Release 未准入而拒絕交付合法的作者候選小包**。

**權限**：只能讀使用者授權來源並寫新的隔離 OutputRoot。不得寫原 Repo/Host、改 Original Oracle、發 Grant、冒 Original Checker/Publisher 簽章，也不要執行 W0 的 Native Effect。本輪作者完成上限 `AUTHOR_CONTROL_PACK_CANDIDATE_WITH_NAMED_HOLDS`；任何本地 guard PASS 也只算 `AUTHOR_LOCAL_LINKS_ONLY`。

**交付**：請直接建立真實檔案、逐檔讀回後提供 **十五個檔案及獨立證據 MD 的下載載點**（每檔 bytes＋SHA256）；最終以簡表呈現 15/15 狀態、W0-A/B/C、PK-Q01..14 實際結果、受影修補、Original Domain 未綁事項與下一步最小 Resume。缺某來源時完成可有源部分並清楚列 HOLD；不要只交工作計畫、未寫入的檔名表、假載點或預定成果。

---

**預期文件身份**：`FHS-5_PLP_W0/` 下固定十五檔；另 `FHS-5_PLP_W0_證據型附錄.md`。如果環境可用，只執行已由本地 Work 明確授權的檔案操作，不做越權 Host 工作。
