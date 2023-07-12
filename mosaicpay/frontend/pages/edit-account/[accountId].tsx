import {
	Alert,
	Box,
	Button,
	Container,
	FormControl,
	Grid,
	TextField,
	Typography,
} from "@mui/material";
import { Cancel, Delete, Garage, Save, Upload } from "@mui/icons-material";
import { useEffect, useState } from "react";
import * as yup from "yup";
import {
	deleteAccount,
	getAccount,
	getDocument,
	getUser,
	putAccount,
} from "../../src/app/api";
import { useRouter } from "next/router";
import AccountInfoCard from "@/app/components/AccountInfoCard";
import AccountMenu from "@/app/components/AccountMenu";
import Media from "@/app/components/Media";

export default function NewAccount() {
	const router = useRouter();
	const { accountId } = router.query;

	const [accountName, setAccountName] = useState("");
	const [balance, setBalance] = useState("");
	const [validationErrors, setValidationErrors] = useState(Object);
	const [showAlert, setShowAlert] = useState(false);
	const [alertMessage, setAlertMessage] = useState("");
	const [userId, setUserId] = useState(0);
	const [type, setType] = useState("");
	const [url, setUrl] = useState();
	const [documentId, setDocumentId] = useState(0);
	const getAccountData = async () => {
		//@ts-ignore
		const accountData = await getAccount(Number.parseInt(accountId));
		return accountData;
	};
	let data: dtoAccount;
	const setStates = async () => {
		try {
			if (accountId) {
				data = await getAccountData();
				setAccountName(data?.name);
				setBalance(data?.balance.toString());
				setUserId(data.user);
				const document: any = await getDocument(accountId);
				setType(document.type);
				setUrl(document.url);
				setDocumentId(document.document_id);
			}
		} catch (error: any) {
			if (error.response.status === 500) {
				return;
			}
		}
	};

	useEffect(() => {
		setStates();
	}, [accountId, documentId]);

	const validationSchema = yup.object().shape({
		accountName: yup
			.string()
			.required("Account name is required")
			.max(255, "Maximum length of the account name is 255 characters")
			.min(5, "Minimum length of the account name is 5"),
		balance: yup
			.number()
			.typeError("Balance must be a number")
			.required("Balance is required"),
	});

	const handleAccountNameChange = (event: any) => {
		const inputValue = event.target.value;
		if (inputValue !== data?.name) {
			setAccountName(inputValue);
		}
	};

	const handleBalanceChange = (event: any) => {
		setBalance(event.target.value);
	};

	const validateForm = async (): Promise<boolean> => {
		try {
			await validationSchema.validate(
				{ accountName, balance },
				{ abortEarly: false }
			);
			setValidationErrors({});
			return true;
		} catch (error: any) {
			const errors = {};
			error.inner.forEach((err: any) => {
				//@ts-ignore
				errors[err.path] = err.message;
			});
			setValidationErrors(errors);
			return false;
		}
	};
	const handleSubmit = async (event: any) => {
		event.preventDefault();
		if (await validateForm()) {
			try {
				let account: dtoAccountUpdate = {
					name: accountName,
					balance: Number.parseFloat(balance),
				};
				//@ts-ignore
				await putAccount(Number.parseInt(accountId), account);
				setShowAlert(true);
				setAlertMessage("Account successfuly updated!");
				setStates();
				return;
			} catch (error) {}
		}
	};

	const handleDelete = async () => {
		try {
			await deleteAccount(accountId);
			setShowAlert(true);
			setAlertMessage("Account is successfuly deleted!");
		} catch (error) {}
	};

	return (
		<Container disableGutters>
			<Box mb={5} display={"flex"} justifyContent={"center"}>
				<AccountMenu></AccountMenu>
			</Box>
			<Grid
				display="flex"
				flexDirection="column"
				width="100%"
				height="100%"
				justifyContent="center"
			>
				<Box
					margin={2}
					pb={3}
					width={"100%"}
					display={"flex"}
					flexDirection={"row"}
					justifyContent={"center"}
				>
					<AccountInfoCard
						balance={balance}
						date={new Date().toDateString()}
						showDetail={false}
					></AccountInfoCard>
				</Box>
				<Box width="100%" padding={2}>
					<TextField
						sx={{ mb: 2 }}
						fullWidth
						id="account-name"
						name="accountName"
						label="Account name"
						placeholder="Savings account"
						variant="outlined"
						color="secondary"
						value={accountName}
						onChange={(e: any) => {
							handleAccountNameChange(e);
						}}
						error={!!validationErrors.accountName}
						helperText={validationErrors.accountName}
					/>

					<TextField
						sx={{ mb: 2 }}
						fullWidth
						id="balance"
						name="balance"
						placeholder="784578.45"
						label="Balance"
						variant="outlined"
						color="secondary"
						value={balance}
						onChange={handleBalanceChange}
						error={!!validationErrors.balance}
						helperText={validationErrors.balance}
					/>

					<Box display={"flex"} justifyContent={"center"} sx={{ mt: 5 }}>
						<Media
							accountId={accountId!.toString()}
							userId={userId?.toString()}
							url={url}
							type={type}
							documentId={documentId}
						></Media>
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
						{alertMessage}
					</Alert>
					<Box
						display={"flex"}
						justifyContent={"space-between"}
						sx={{ mt: 10 }}
					>
						<Button
							startIcon={<Save></Save>}
							color="secondary"
							variant="outlined"
							onClick={(e: any) => handleSubmit(e)}
						>
							Save
						</Button>
						<Button
							startIcon={<Delete></Delete>}
							color="secondary"
							variant="outlined"
							onClick={() => handleDelete()}
						>
							Delete
						</Button>
					</Box>
				</Box>
			</Grid>
		</Container>
	);
}
