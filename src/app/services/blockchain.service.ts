import { Injectable } from '@angular/core';
import { BlockChain } from '4pjt/blockchain';
import EC from 'elliptic';
@Injectable({
  providedIn: 'root'
})
export class BlockchainService {
  public blockChainInstance = new BlockChain();
  public walletKeys: Array<IWalletKey> = [];
  constructor() {
    this.blockChainInstance.difficulty = 1;
    this.blockChainInstance.minePendingTransaction('hi');
    this.generateWalletKeys();
  }

  minePendingTransactions() {
    this.blockChainInstance.minePendingTransactions(
      this.walletKeys[0].publicKey
    );
  }

  addressIsFromCurrentUser(address) {
    return address === this.walletKeys[0].publicKey;
  }

  generateWalletKeys() {
    const ec = new EC.ec('secp256k1');
    const key = ec.genKeyPair();
    console.log(key.getPublic('hex'));
    console.log(key.getPrivate('hex'));

    this.walletKeys.push({
      keyObj: key,
      publicKey: key.getPublic('hex'),
      privateKey: key.getPrivate('hex')
    });

    console.log(this.walletKeys);
  }

  getPendingTransactions() {
    return this.blockChainInstance.pendingTransactions;
  }

  addTransaction(tx) {
    this.blockChainInstance.addTransaction(tx);
  }
}

export interface IWalletKey {
  keyObj: any;
  publicKey: string;
  privateKey: string;
}
