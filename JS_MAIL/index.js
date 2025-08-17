const Imap = require('node-imap');

const args = process.argv.slice(2); // เริ่มต้นตัดออกแถวแรกที่ node และชื่อไฟล์

let username, password, findMail;
for (let i = 0; i < args.length; i++) {
    if (args[i] === '-u' && i + 1 < args.length) {
        username = args[i + 1];
    } else if (args[i] === '-p' && i + 1 < args.length) {
        password = args[i + 1];
    }
    else if (args[i] === '-f' && i + 1 < args.length) {
        findMail = args[i + 1];
    }
}

if (!username || !password || !findMail) return console.log("Wrong Input Data!")

// ตั้งค่าเชื่อมต่อ IMAP
const imapConfig = {
    user: username, //'Auto.esol1@gmail.com',
    password: password, //'ywwr gmxx hfig mrsv',
    host: 'imap.gmail.com',
    port: 993,
    tls: true
};

// กำหนดคำค้นหาที่ต้องการ
const searchTerm = findMail; //'รหัสอ้างอิง คือ EALGD'; // เปลี่ยน 'your_search_query' เป็นคำค้นหาที่ต้องการ

// สร้าง client สำหรับเชื่อมต่อกับเซิร์ฟเวอร์ IMAP
const imap = new Imap(imapConfig);

imap.connect();

imap.once('ready', function() {
    imap.openBox('INBOX', true, function(err, box) {
        if (err) throw err;

        // ค้นหาอีเมล์ที่มีข้อความที่ตรงกับคำค้นหา
        imap.search([['TEXT', searchTerm]], function(err, results) {
            if (err) throw err;

            if (results.length === 0) {
                console.log('No emails found matching the search criteria.');
                imap.end();
                return;
            }
           
            // เลือกเฉพาะเมล์แรกที่ตรงเงื่อนไข
            const fetch = imap.fetch(results, { bodies: ['TEXT'] });

            fetch.on('message', function(msg, seqno) {
                let body = '';
                msg.on('body', function(stream, info) {;
                    stream.on('data', function(chunk) {
                        body += chunk.toString('utf8');
                    });
                });

                msg.once('attributes', function(attrs) {});

                msg.once('end', function() {
                    const startMarker = 'Content-Transfer-Encoding: base64';
                    const endMarker = '------=_Part_';

                    if (body.indexOf(startMarker) > 0) {
                        const startIndex = body.indexOf(startMarker) + startMarker.length;
                        let base64Content = body.substring(startIndex).trim();
                        const endIndex = base64Content.indexOf(endMarker);
                        base64Content = base64Content.substring(0, endIndex).trim();
                        // ดึงเฉพาะเนื้อหาที่เป็น base64
                        const buffer = Buffer.from(base64Content, 'base64');
                        decodedText = buffer.toString('utf-8');
                        //console.log(decodedText)
                    }
                    else decodedText = body
                    const regex = /\b\d{6}\b/g;
                    const numbers = decodedText.match(regex);
                    console.log(numbers[0]);
                });
            });

            fetch.once('error', function(err) {
                console.error('Fetch error:', err);
            });

            fetch.once('end', function() {
                imap.end();
            });
        });
    });
});

imap.once('error', function(err) {
    console.error('IMAP error:', err);
});

imap.once('end', function() {
    //console.log('IMAP connection ended.');
});
