const axios = require('axios');
const baseURL = 'http://activist-birds.picoctf.net:54131/check';  // Replace with the actual URL

const tryCircuit = async (input1, input2) => {
    try {
        const response = await axios.post(baseURL, {
            circuit: [
                { input1, input2, output: input1 ^ input2 }
            ]
        });

        console.log(`Tried: input1 = ${input1}, input2 = ${input2} -> ${response.data.flag}`);
        if (response.data.flag.includes("FLAG2")) {
            console.log("Flag 2 Found!");
            process.exit();
        }
    } catch (error) {
        console.error("Request failed", error);
    }
};

const bruteForce = async () => {
    for (let input1 = 1; input1 <= 255; input1++) {
        for (let input2 = 1; input2 <= 255; input2++) {
            await tryCircuit(input1, input2);
        }
    }
};

bruteForce();
