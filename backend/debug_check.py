import zipfile, os, re

# Find the latest output file
output_dir = 'outputs'
files = [f for f in os.listdir(output_dir) if f.endswith('.docx')]
files.sort(key=lambda f: os.path.getmtime(os.path.join(output_dir, f)))
latest = os.path.join(output_dir, files[-1])
print(f'Latest output: {latest}')

z = zipfile.ZipFile(latest, 'r')
doc_xml = z.read('word/document.xml').decode('utf-8', errors='ignore')
print(f'Doc XML length: {len(doc_xml)}')
has_vinod = 'Vinod' in doc_xml
has_gangadhar = 'GANGADHAR' in doc_xml
print(f'Contains Vinod: {has_vinod}')
print(f'Contains GANGADHAR: {has_gangadhar}')

# Show first 20 text nodes
texts = re.findall(r'<w:t[^>]*>([^<]+)</w:t>', doc_xml)
print(f'First 20 text nodes:')
for i, t in enumerate(texts[:20]):
    print(f'  [{i}]: {t}')
z.close()
