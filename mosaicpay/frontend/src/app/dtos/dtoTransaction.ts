class dtoTransaction {
	type: string;
	amount: number;
	account: number;
	transaction_state: number;

	constructor() {
		this.type = "d";
		this.amount = 0;
		this.account = 0;
		this.transaction_state = 0;
	}
}
