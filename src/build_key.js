// Answer key for the Module 1 practice lab exam.
// Reads the question table dumped by data.py, writes a Letter portrait DOCX.
const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
} = require('docx');

const D = JSON.parse(fs.readFileSync('/root/t3/out/questions.json', 'utf8'));
const NAVY = '1E3D4C', TERRA = '8B3A2E', MUTED = '4A5A63', LINE = 'D7DDE0';
const COLS = [760, 2960, 3200, 2440];            // sums to 9360 DXA
const TOTAL = COLS.reduce((a, b) => a + b, 0);

function cell(children, width, shade) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: shade ? { type: ShadingType.CLEAR, fill: shade } : undefined,
    margins: { top: 90, bottom: 90, left: 110, right: 110 },
    children,
  });
}
function p(text, opts = {}) {
  return new Paragraph({
    spacing: { after: opts.after === undefined ? 0 : opts.after },
    children: [new TextRun({
      text,
      bold: !!opts.bold,
      color: opts.color || NAVY,
      size: opts.size || 19,                     // half points
      font: 'Aptos',
    })],
  });
}

const header = new TableRow({
  tableHeader: true,
  children: [
    cell([p('No.', { bold: true, color: 'FFFFFF' })], COLS[0], NAVY),
    cell([p('Question', { bold: true, color: 'FFFFFF' })], COLS[1], NAVY),
    cell([p('Answer', { bold: true, color: 'FFFFFF' })], COLS[2], NAVY),
    cell([p('Also accepted', { bold: true, color: 'FFFFFF' })], COLS[3], NAVY),
  ],
});

const rows = [header];
let gapDone = false;
for (const q of D.questions) {
  if (!gapDone && q.n > D.pending[0]) {
    rows.push(new TableRow({
      children: [cell([p('Questions ' + D.pending[0] + ' to '
        + D.pending[D.pending.length - 1]
        + ' are not in this version. Three slides are still to come.',
        { color: TERRA, bold: true })], TOTAL, 'FBF7EF')],
    }));
    gapDone = true;
  }
  rows.push(new TableRow({
    children: [
      cell([p(String(q.n), { bold: true, color: TERRA })], COLS[0]),
      cell([p(q.tag)], COLS[1]),
      cell([p(q.a, { bold: true })], COLS[2]),
      cell([p((q.alt || []).join(', '), { color: MUTED, size: 17 })], COLS[3]),
    ],
  }));
}

const doc = new Document({
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1080, bottom: 1080, left: 1440, right: 1440 },
      },
    },
    children: [
      new Paragraph({
        spacing: { after: 40 },
        children: [new TextRun({
          text: (D.course + '  ·  ' + D.school).toUpperCase(),
          color: TERRA, bold: true, size: 17, font: 'Aptos',
        })],
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { after: 80 },
        children: [new TextRun({
          text: D.title + ', Answer Key',
          color: NAVY, bold: true, size: 34, font: 'Aptos',
        })],
      }),
      p('The answer in bold is what the grader marks right. Everything in the '
        + 'last column is accepted too. Extra words do not cost anything. '
        + 'A misspelled structure does, the same as it would on the practical.',
        { color: MUTED, after: 260 }),
      new Table({
        columnWidths: COLS,
        width: { size: TOTAL, type: WidthType.DXA },
        borders: {
          top: { style: BorderStyle.SINGLE, size: 4, color: LINE },
          bottom: { style: BorderStyle.SINGLE, size: 4, color: LINE },
          left: { style: BorderStyle.SINGLE, size: 4, color: LINE },
          right: { style: BorderStyle.SINGLE, size: 4, color: LINE },
          insideHorizontal: { style: BorderStyle.SINGLE, size: 4, color: LINE },
          insideVertical: { style: BorderStyle.SINGLE, size: 4, color: LINE },
        },
        rows,
      }),
      new Paragraph({
        spacing: { before: 320 },
        alignment: AlignmentType.LEFT,
        children: [new TextRun({
          text: D.byline, color: NAVY, bold: true, size: 19, font: 'Aptos',
        })],
      }),
    ],
  }],
});

const OUT = '/root/t3/out/Module-1-Practice-Lab-Exam-KEY.docx';
const PDF = OUT.replace(/\.docx$/, '.pdf');

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(OUT, buf);
  console.log('key written, ' + Math.round(buf.length / 1024) + ' KB, '
    + D.questions.length + ' questions');

  // Refresh the PDF in the same breath. Leaving it to a separate step once let
  // a stale PDF from an earlier build ship beside a corrected DOCX, which is
  // the worst kind of bug: both files look fine on their own.
  try {
    if (fs.existsSync(PDF)) fs.unlinkSync(PDF);
    require('child_process').execFileSync('python3', [
      '/mnt/skills/public/docx/scripts/office/soffice.py',
      '--headless', '--convert-to', 'pdf', OUT,
    ], { cwd: '/root/t3/out', stdio: 'ignore' });
    console.log('pdf refreshed, ' + Math.round(fs.statSync(PDF).size / 1024) + ' KB');
  } catch (e) {
    console.log('PDF NOT REFRESHED, convert it by hand before shipping');
  }
});
