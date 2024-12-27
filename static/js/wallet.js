import { PeraWalletConnect } from "@perawallet/connect";
import algosdk from "algosdk";

const peraWallet = new PeraWalletConnect({
    shouldShowSignTxnToast: true
});

const algorand = new algosdk.Algodv2(
    "",
    "https://mainnet-api.algonode.cloud",
    ""
);

export async function connectWallet() {
    try {
        const accounts = await peraWallet.connect();
        return accounts[0];
    } catch (error) {
        console.error("Cüzdan bağlantı hatası:", error);
        return null;
    }
}

export { peraWallet, algorand };