import { Account } from "./account.js";
import { LimitedWithdraw } from "./limitedWithdraw.js";
import { MovementsAccount } from "./movementsAccount.js";

export class AccountFactory {
    static createNewAccount(balance, salary, movements, movementsToday, lastMovement) {
        const account = new Account(balance, salary)
        const limitedAccount = new LimitedWithdraw(account)
        return new MovementsAccount(limitedAccount, movements, movementsToday, lastMovement)
    }
}