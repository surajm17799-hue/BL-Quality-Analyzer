def build_spec_title_prompt(display_id, title,specs,isq_asked,isq_filled):  
    prompt = f"""
You are an intelligent buylead quality correction assistant.
Detect and fix contradictions between **Buylead title** and **buyer-filled ISQ values**.
### INPUT
- eto_ofr_display_id: {display_id}
- eto_ofr_title: {title}
- isq_asked: {isq_asked}
- isq_filled: {isq_filled}

### RULES
1. 🔥 ONLY MODIFY IF THERE IS A DIRECT, UNAMBIGUOUS CONTRADICTION
2. ❌ NEVER ENRICH, APPEND, OR ADD NEW DETAILS
3. 🔒 IGNORE contradictions in brand, model, part number, grade, or variant
4. ✅ ONLY REPLACE the conflicting term, preserve structure
5. 📏 Normalize for comparison (case, spacing, synonyms, units) but not in output
6. 🚫 DO NOT CHANGE IF:
   - ISQ adds new info not in title
   - Difference is only formatting/case
   - Values are synonyms/equivalent units
   - Contradiction is only brand/model/grade
7. ✅ CHANGE ONLY IF:
   - Attribute is in title
   - After normalization, values are factually different
   - Attribute impacts product’s core specification (size, capacity, material, strength, power, etc.)

### OUTPUT 
eto_ofr_display_id, enriched_title, mismatch, mismatch_details

- enriched_title → modified title only if contradiction exists, else same as original
- mismatch → 1 if changed, 0 if not
- mismatch_details → if changed, describe contradiction as:
  "{{Attribute}}: '{{value_in_title}}' (title) contradicted by '{{value_in_isq}}' (ISQ)"

### EXAMPLES
✅ Change:
- "50mm Cement Paver Block" vs ISQ: "30 mm" → "30 mm Cement Paver Block"
- "1kg Ginger Garlic Paste" vs ISQ: "200 g" → "200 g Ginger Garlic Paste"

❌ No Change:
- "Sliding Window" vs ISQ: "Aluminium" → no change
- "Tata Tea Gold" vs ISQ: "Tata Tea Agni" → no change
- "MS Garden Plant Stand" vs ISQ: "Iron" → no change (MS ≈ Mild Steel ≈ Iron)

### OUTPUT (JSON):
{{ "display_id": "{display_id}",
    "new_title": "<corrected_or_original_title>",
    "mismatch_found": <0 or 1> }}
"""
    return prompt

def build_one_word_title_prompt(display_id, title,glcat_mcat_name,isq_asked,isq_filled):
    prompt = f"""
Your task is to enhance a one-word product title (eto_ofr_title) so that it becomes clear, specific, and SEO-friendly, using buyer-provided buyer_filled_details values and the mapped category(glcat_mcat_name) name.
---
### INPUT
- eto_ofr_display_id: {display_id}
- eto_ofr_title: {title}
- glcat_mcat_name: {glcat_mcat_name}
- isq_asked: {isq_asked}
- isq_filled: {isq_filled}

### ENRICHMENT RULES
1. 🔒 **Preserve original keywords**  
   Never delete or replace important terms (e.g., "Redmi" must remain).   

2. ✅ **Enrich with ISQ values**  
   - Add relevant `buyer_filled_details` values before/after the title.
   - **For mobiles**: Use attribute labels (e.g., `"32 GB ROM 3 GB RAM Redmi"`).  
   - **For others**: Add values without labels if clearly understood (e.g., `"1 mm Guns"`).

3. 🚫 **Avoid redundancy**  
   - Drop duplicates/synonyms (e.g., `"Wheat"` + `"Gehu"` → use only `"Gehu"`).
   - Ignore vague buyer_filled_details like `"Other Details"`.

4. 🧭 **Fallback to category**  
   Use `glcat_mcat_name` only if:
   - It's >1 word AND not already in the title
   - buyer_filled_details data is missing or irrelevant
5. **Consider only sensible and relevant ISQ**  
   - Use only meaningful buyer_filled_details values from BL details that directly enhance Quality of the one-word title  
   - It is not mandatory to include every specification present in BL details  

6. 🎯 **Special cases**  
   - **Remove hyphens** from non-chemical names (`"Rum-Pum-Noodles"` → `"Rum Pum Noodles"`)  
   - **Preserve hyphens** in chemicals (`"1-(dichloromethyl)-benzene"`)  
   - **Preserve brand/model names exactly** (e.g., `"LS24C330GAWXXL"`).

### OUTPUT (JSON):
{{ "display_id": "{display_id}",
 "enhanced_title": "<enriched_or_original_title>", 
 "one_word_issue": <0 or 1> }}
"""
    return prompt

def build_pii_check_prompt(display_id,title, description,isq_asked,isq_filled):
    prompt = f"""
You are an intelligent buylead quality assistant.
Your task is to **detect and remove PII (Personally Identifiable Information)** from the record to protect privacy.

### INPUT
- display_id: {display_id}
- eto_ofr_title: {title}
- eto_ofr_description: {description}
- isq_asked: {isq_asked}
- isq_filled: {isq_filled}

### LOGIC
1. Scan enriched_title, eto_ofr_description, buyer_filled_details, and isq_filled for common PII patterns.
2. PII Examples (Strict Patterns to flag):
   - Mobile numbers: 10-digit sequences (e.g., "9876543210", "91-9876543210").
   - Email addresses: (e.g., "user@example.com").
   - Credit card numbers: 16-digit sequences, often with specific prefixes.
   - GSTIN/PAN numbers: GSTIN = 15-digit alphanumeric, PAN = 10-character alphanumeric.
   - Contact requests: "whatsapp me", "call me at", "contact me on" followed by number/email.
3. Do NOT flag:
   - Generic phrases like "seller number", "contact details", "Whatsapp" without numbers/emails.
   - Partial numbers (like "91" alone).
   - Company names or generic addresses.
4. Removal: If PII is found, remove/redact it from the fields.

### OUTPUT (JSON):
{{
  "display_id": "{display_id}",
  "pii": <0 or 1>,
  "pii_details": "<comma_separated_types_and_sources_if_found>", 
  "cleaned_title": "<title_without_pii>",
  "cleaned_description": "<description_without_pii>",
  "": "<buyer_details_without_pii>",
  "cleaned_isq_filled": "<isq_without_pii>"
}}
"""
    return prompt
def build_selling_intent_prompt(display_id, title,description,isq_filled):
    prompt = f"""
You are an intelligent buylead classification assistant.  
Your objective is to determine whether the input record represents a **Selling Requirement** (seller offering a product) or a **Buying Requirement** (buyer looking to purchase).  

### INPUT
- eto_ofr_display_id: {display_id}
- eto_ofr_title: {title}
- eto_ofr_description: {description}
- isq_filled: {isq_filled}
### DECISION LOGIC
1. **Strict Selling Keywords/Phrases → High Confidence (sells=1)**
   Examples:  
   "Want to Sell", "sell my", "selling my", "mujhe sell karni h", "I am Seller",  
   "I want to sell", "I am selling", "Old Currency Selling", "Currency Selling",  
   "note sale", "note sell", "for sell" (only if used as direct offer).  

2. **Contextual Selling Inference**
   - If user explicitly states they are a seller or offering a product → sells=1.  

3. **Buying Keywords/Phrases → Do NOT Flag as Selling (sells=0)**  
   Examples:  
   - "I only want ... for selling"  
   - "I am online seller so I want best quality ..."  
   - "We need ..."  
   - "... t shirt for sell" (means buyer wants to buy to resell)  
   - "Which product do u sell ..."  
   - "Looking for reliable suppliers"  
   - "I want to resell"  
   - "Want to sell in my shop"  
   - "for reselling"  
   - "do u sell"  
   - "amazon par sell karna hai"  
   - "seller number"  
   - "wholeseller"  

4. **Generic Terms (Not Selling Alone)**  
   Words like "sell", "selling", "reseller", "wholesale", "supplier",  
   "manufacturer", "trader", "distributor", "vendor" do NOT mean selling intent unless matched with strict rules.  

5. **Special Rule: `eto_ofr_modref_dispname`**
   - If a selling keyword is in `eto_ofr_title` but the title is identical to `eto_ofr_modref_dispname` → classify as **buying (sells=0)**.  
   - Unless strict selling phrases are also present in description.  


### OUTPUT (JSON):
{{ "display_id": "{display_id}", "selling_intent_issue": <0 or 1> }}
"""
    return prompt
