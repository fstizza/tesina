import { ChangePassword } from "./changePassword.js";
import { User } from "./user.js";

export class UserFactory {
    static createNewUser(name, password, lastChange){
        const user = new User(name, password)
        return new ChangePassword(user, lastChange)
    }
}