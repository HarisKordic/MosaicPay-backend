import React, { useState } from "react";
import {
	Alert,
	Box,
	Button,
	Container,
	FormControlLabel,
	Grid,
	InputLabel,
	MenuItem,
	Radio,
	RadioGroup,
	Select,
	Slider,
	Typography,
} from "@mui/material";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { getUserAccounts, postNewTransaction } from "../../src/app/api";
import { Cancel, Save } from "@mui/icons-material";
import AccountMenu from "@/app/components/AccountMenu";

export default function NewTransaction() {
	const [showAlert, setShowAlert] = useState(false);
	const [transactionState, setTransactionState] = useState(1);
	const [accountState, setAccountState] = useState([]);
	const [selectedAccount, setSelectedAccount] = useState("");
	const [amountState, setAmountState] = useState(1000);

	const [transactionType, setTransactionType] = useState("d");
	const router = useRouter();

	useEffect(() => {
		const getData = async () => {
			const data = await getUserAccounts();
			const accounts = data.map((item: any) => ({
				value: item.account_id,
				name: item.name,
			}));
			setAccountState(accounts);
			if (accounts.length > 0) {
				setSelectedAccount(accounts[0].value);
			}
		};

		getData();
	}, []);

	const handleSubmit = async () => {
		try {
			const transaction: dtoTransaction = {
				type: transactionType,
				amount: amountState,
				account: Number.parseInt(selectedAccount),
				transaction_state: transactionState,
			};
			await postNewTransaction(transaction);

			setShowAlert(true);

			setTimeout(() => {
				router.push("/home");
			}, 2000);
		} catch (error) {}
	};

	const handleAccountChange = (event: any) => {
		setSelectedAccount(event.target.value);
	};

	return (
		<Container>
			<Box display={"flex"} justifyContent={"center"} mb={5}>
				<AccountMenu></AccountMenu>
			</Box>
			<Grid
				display="flex"
				flexDirection="column"
				width="100%"
				height="100%"
				justifyContent="center"
			>
				<Box>
					<Typography variant="h4" component="h4" sx={{ textAlign: "center" }}>
						Add transaction
					</Typography>
				</Box>
				<Box width="100%" padding={2}>
					<Box mt={3}>
						<InputLabel id="transaction-state-simple-select-label">
							Transaction type
						</InputLabel>
						<RadioGroup
							aria-labelledby="transaction-type-radio-buttons-group-label"
							defaultValue="d"
							name="transaction-type-radio-buttons-group"
							onChange={(event) => setTransactionType(event.target.value)}
						>
							<FormControlLabel
								value="d"
								control={<Radio color="secondary" />}
								label="Debit"
							/>
							<FormControlLabel
								value="c"
								control={<Radio color="secondary" />}
								label="Credit"
								color="secondary"
							/>
						</RadioGroup>
					</Box>
					<Box mt={3}>
						<InputLabel>Amount</InputLabel>
						<Slider
							max={10000}
							size="medium"
							defaultValue={1000}
							aria-label="Medium"
							valueLabelDisplay="auto"
							color="secondary"
							onChange={(e: any) => setAmountState(e.target.value)}
						/>
					</Box>
					<Box mt={3}>
						<InputLabel id="account-state-simple-select-label">
							Account
						</InputLabel>
						<Select
							fullWidth
							labelId="account-state-select-label"
							id="account-state-select"
							name="account-state"
							value={selectedAccount}
							label="Account state"
							onChange={handleAccountChange}
							color="secondary"
						>
							{accountState.map((account: any) => (
								<MenuItem value={account.value} key={account.value}>
									{account.name}
								</MenuItem>
							))}
						</Select>
					</Box>
					<Box mt={3}>
						<InputLabel id="transaction-state-simple-select-label">
							Transaction state
						</InputLabel>
						<Select
							fullWidth
							labelId="transaction-state-select-label"
							id="transaction-state-select"
							name="transaction-state"
							value={transactionState}
							label="Transaction state"
							onChange={(e: any) => setTransactionState(e.target.value)}
							color="secondary"
						>
							<MenuItem value={1}>Draft</MenuItem>
							<MenuItem value={2}>Pending</MenuItem>
							<MenuItem value={3}>Processed</MenuItem>
							<MenuItem value={4}>Failed</MenuItem>
						</Select>
					</Box>

					<Box
						display={"flex"}
						justifyContent={"space-between"}
						sx={{ mt: 10 }}
					>
						<Button
							startIcon={<Save></Save>}
							color="secondary"
							variant="outlined"
							onClick={handleSubmit}
						>
							Save
						</Button>
						<Button
							startIcon={<Cancel></Cancel>}
							color="secondary"
							variant="outlined"
							onClick={() => router.push("/home")}
						>
							Cancel
						</Button>
					</Box>
				</Box>
				<Alert
					sx={{ mt: 5, display: showAlert ? "flex" : "none" }}
					action={
						<Button
							color="success"
							size="small"
							onClick={() => setShowAlert(false)}
						>
							X
						</Button>
					}
					onClose={() => setShowAlert(false)}
					severity="success"
				>
					Transaction successfully created!
				</Alert>
			</Grid>
		</Container>
	);
}
