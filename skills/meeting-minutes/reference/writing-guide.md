# Writing guide for minutes

## Voice

- Past tense, third person, neutral: "The team agreed to…", "K. Nok will…". No "I think", no adjectives about people.
- One idea per sentence. Short sentences. Numbers as digits. Dates as `2026-10-18` or `18 Oct`, never "next Friday".
- Record outcomes, not the conversation. "Discussed pricing for 20 minutes" says nothing; "Agreed to keep the ฿299 plan and test ฿349 with new sign-ups in November" does.
- Attribute decisions to the role or group that made them ("Product owner approved…"), attribute opinions only when it matters for the record and the person would not mind reading it.
- Keep disagreement factual: "A preferred X because …; B preferred Y because …; no decision, revisit on 25 Oct."

## Decisions

Good: `D3. Use PostgreSQL for the reporting store instead of adding ClickHouse now; revisit when daily rows exceed 50M. (CTO, 00:32:10)`
Bad: `Talked about databases, PostgreSQL seems fine.`

## Action items

- Start with a verb: "Send", "Draft", "Decide", "Book", "Fix".
- One owner (a person, not "team"). If two people, two rows.
- Due date or "before <event>". If none was said: `(date?)`.
- Testable: someone can say yes/no it was done.
- Source: timestamp or slide, so the owner can check context.

## Thai meetings

- เขียนภาษาไทยแบบทางการแต่สั้น ใช้ศัพท์เทคนิคภาษาอังกฤษตามที่พูดจริง ไม่แปลชื่อระบบ ชื่อฟีเจอร์ ชื่อ ticket
- ชื่อคนใช้ตามที่เรียกในประชุม (คุณนก, พี่เอ) และคงรูปเดิมทั้งเอกสาร
- หัวข้อ "สรุปสั้น" ไม่เกิน 5 บรรทัด ผู้บริหารอ่านแล้วรู้ผลลัพธ์ทันที
- Action item ใช้ตาราง ลำดับ | งาน | ผู้รับผิดชอบ | กำหนด | อ้างอิง

## Length

| Meeting | Minutes |
|---|---|
| 15-min stand-up | ½ page: blockers, changes, actions |
| 1-hour working session | 1–2 pages |
| Half-day workshop | 3–4 pages with an index of topics; decisions and actions first |

## What to leave out

Small talk, repeated points, who was late, tangents that produced nothing, verbatim quotes longer than one sentence, anything personal or confidential unless the meeting was about it and the audience is right.

## Anti-patterns

- Minutes that read like a transcript with timestamps every line.
- "Various options were discussed" without saying which.
- Actions assigned to people who were not in the meeting without noting it.
- Summaries that upgrade "maybe" to "will".
- A TL;DR that is a list of topics instead of outcomes.
