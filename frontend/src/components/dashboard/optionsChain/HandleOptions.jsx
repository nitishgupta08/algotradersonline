import React, {useContext, useEffect, useState} from "react";
import {
    Box,
    Button,
    Card,
    FormControl,
    FormControlLabel,
    Grid,
    Radio,
    RadioGroup,
    TextField,
    Typography,
    Snackbar,
    Alert
} from "@mui/material";
import {BaseURL} from "../../../BaseURL";
import {UserContext} from "../../../UserContext";
import OptionsTable from "./OptionsTable";
import {AdapterDayjs} from '@mui/x-date-pickers/AdapterDayjs';
import {LocalizationProvider} from '@mui/x-date-pickers/LocalizationProvider';
import {DateTimePicker} from '@mui/x-date-pickers/DateTimePicker';
import ArrowDropUpIcon from '@mui/icons-material/ArrowDropUp';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';

const HandleOptions = () => {
    const {user} = useContext(UserContext);
    const juser = JSON.parse(user);
    const [data, setData] = useState(null);
    const [histo, setHisto] = useState(null);
    const [spot, setSpot] = useState(18000);
    const [value, setValue] = useState("latest");
    const [date, setDate] = useState(new Date());
    const [open,setOpen] = useState(false);

    const snackBarClose = () => {
        setOpen(false);
    };

    const getData = () => {
        fetch(BaseURL + "api/get_nifty/", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Token ${juser.data.token}`,
            },
        })
            .then((response) => {
                if (response.ok === true) return response.json();
                else {
                    throw new Error();
                }
            })
            .then((rData) => {
                setData(rData);
            })
            .catch((error) => {
                setOpen(true);
                console.log(error);
            });
    }

    const getHisto = () => {
        const request = {date: date};

        fetch(BaseURL + "api/get_nifty_histo/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Token ${juser.data.token}`,
            },
            body: JSON.stringify(request)
        })
            .then((response) => {
                if (response.ok === true) return response.json();
                else {
                    throw new Error();
                }
            })
            .then((rData) => {
                setHisto(rData);
            })
            .catch((error) => {
                setOpen(true);
                console.log(error);
            });
    }

    const [filter, setFilter] = useState({
        pcr: true,
        cpr: true,
        sos: false,
        rw: false,
        bs: false,
        sl: false,
        is: false,
        ss: false,
        pcrw: false,
        cprw: false,
        pcoc: true,
        pco: true,
    });

    useEffect(() => {
        getData();
        const interval = setInterval(() => {
            getData();
        }, 15000);
        return () => clearInterval(interval);
        // eslint-disable-next-line
    }, []);

    return (
        <>
            <Snackbar
                open={open}
                autoHideDuration={5000}
                onClose={snackBarClose}
                anchorOrigin={{ vertical: "bottom", horizontal: "right" }}>
                <Alert severity="error" variant="filled">
                    Server Error. Cannot fetch data. Please try again later.
                </Alert>
            </Snackbar>
            <Card
                sx={{
                    borderRadius: 1.5,
                    boxShadow: "0px 0px 10px 5px rgba(0,0,0,0.1)",
                    p: 2,
                    mt: 2,
                }}>
                <Grid container spacing={2}>
                    <Grid item xs={12}>
                        <Grid container spacing={2}>
                            <Grid item xs={8}>
                                <Box sx={{display: "flex", flexDirection: "column"}}>
                                    <Grid container>
                                        <Grid item xs={3}>
                                            <FormControl sx={{ml: 2}}>
                                                <Typography
                                                    variant="subtitle"
                                                    sx={{fontSize: "0.9rem", fontWeight: 200}}>
                                                    Settings
                                                </Typography>
                                                <RadioGroup
                                                    aria-labelledby="demo-controlled-radio-buttons-group"
                                                    name="controlled-radio-buttons-group"
                                                    row={true}
                                                    value={value}
                                                    onChange={(e) => {
                                                        setValue(e.target.value)
                                                    }}
                                                >
                                                    <FormControlLabel value="latest" control={<Radio/>} label="Latest"/>
                                                    <FormControlLabel value="histo" control={<Radio/>}
                                                                      label="Historical"/>
                                                </RadioGroup>
                                            </FormControl>
                                        </Grid>

                                        <Grid item xs={9} sx={{pt: 1}}>
                                            {value === "histo" && (<Box>
                                                <LocalizationProvider dateAdapter={AdapterDayjs}>
                                                    <DateTimePicker
                                                        renderInput={(params) => <TextField {...params} />}
                                                        label="Select date and time"
                                                        value={date}
                                                        disableFuture={true}
                                                        onChange={(newValue) => {
                                                            setDate(newValue);
                                                        }}
                                                    />
                                                </LocalizationProvider>
                                                <Button
                                                    type="submit"
                                                    variant="contained"
                                                    sx={{
                                                        ml: 5,
                                                        height: "55px",
                                                    }}
                                                    onClick={() => getHisto()}>
                                                    Fetch
                                                </Button>
                                            </Box>)}
                                        </Grid>
                                    </Grid>

                                    <Filters filter={filter} setFilter={setFilter}/>
                                </Box>

                            </Grid>
                            <Grid item xs={4}>
                                <LiveData setSpot={setSpot} user={juser}/>
                            </Grid>
                        </Grid>
                    </Grid>
                    <Grid item xs={12}>
                        {value === "latest" && (<OptionsTable data={data} filter={filter} spot={spot}/>)}
                        {value === "histo" && (<OptionsTable data={histo} filter={filter} spot={spot}/>)}
                    </Grid>
                </Grid>
            </Card>
        </>
    );
}

const LiveData = ({setSpot, user}) => {
    const request = {"instrument": ["NIFTY SPOT", "NIFTY FUT", "INDIA VIX"]}
    const [liveData, setLiveData] = useState(null);

    const getLiveData = () => {
        fetch(BaseURL + "api/get_ltp/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Token ${user.data.token}`,
            },
            body: JSON.stringify(request),
        })
            .then((response) => {
                if (response.ok === true) return response.json();
                else {
                    throw new Error();
                }
            })
            .then((rData) => {
                setLiveData(rData);
                setSpot(Math.floor(rData[0]['ltp'] / 50) * 50); // NIFTY SPOT LTP
            })
            .catch((error) => {
                console.log(error);
            });
    }

    useEffect(() => {
        getLiveData();
        const interval = setInterval(() => {
            getLiveData();
        }, 1000);
        return () => clearInterval(interval);
        // eslint-disable-next-line
    }, []);

    return (
        <Box>
            {liveData && liveData.map((row) => {
                return (
                    <Box key={row.id} sx={{display: "flex", alignItems: "center"}}>
                        <Typography variant="h5" sx={{fontWeight: 500, mr: 2}}>{row["name"]}</Typography>
                        <Typography sx={{mr: 0.25, fontWeight: 700, fontSize: "1.4rem"}}>{row["ltp"]}</Typography>
                        {row["per_chn"] ? (row["per_chn"] >= 0 ? (
                            <ArrowDropUpIcon sx={{fontSize: "1.4rem", color: "green"}}/>) : (
                            <ArrowDropDownIcon sx={{fontSize: "1.4rem", color: "red"}}/>)) : null}
                        {row["chn_prev_day"] && (
                            <Box sx={{display: "flex"}}>
                                <Typography>{row["chn_prev_day"]}</Typography>
                                <Typography sx={{
                                    color: row["per_chn"] >= 0 ? "green" : "red",
                                    mr: 2
                                }}>({row["per_chn"]}%)</Typography>
                            </Box>
                        )}
                        {row["oi_per_chn"] && (
                            <Box sx={{display: "flex"}}>
                                <Typography sx={{fontWeight: 700}}>OI %CNG FUT: &nbsp;</Typography>
                                <Typography>{row["oi_per_chn"]}</Typography>
                            </Box>
                        )}
                    </Box>
                )
            })}
        </Box>
    );

}

const Filters = ({filter, setFilter}) => {

    return (
        <Box>
            <Typography
                variant="subtitle"
                sx={{fontSize: "0.9rem", fontWeight: 200, ml: 2}}>
                Filters
            </Typography>
            <Box sx={{m: 1}}>
                <Button
                    type="submit"
                    variant={filter.pcoc === true ? "contained" : "outlined"}
                    sx={{
                        m: 1,
                    }}
                    onClick={() => setFilter({...filter, pcoc: !filter.pcoc})}>
                    PUT-CALL OI CHNG
                </Button>

                <Button
                    type="submit"
                    variant={filter.pco === true ? "contained" : "outlined"}
                    sx={{
                        m: 1,
                    }}
                    onClick={() => setFilter({...filter, pco: !filter.pco})}>
                    PUT-CALL OI
                </Button>
                <Button
                    type="submit"
                    variant={filter.pcr === true ? "contained" : "outlined"}
                    sx={{
                        m: 1,
                    }}
                    onClick={() => setFilter({...filter, pcr: !filter.pcr})}>
                    PCR
                </Button>

                <Button
                    type="submit"
                    variant={filter.cpr === true ? "contained" : "outlined"}
                    sx={{
                        m: 1,
                    }}
                    onClick={() =>
                        setFilter({...filter, cpr: !filter.cpr})
                    }>
                    CPR
                </Button>
                <Button
                    type="submit"
                    variant={filter.sos === true ? "contained" : "outlined"}
                    sx={{
                        m: 1,
                    }}
                    onClick={() => setFilter({...filter, sos: !filter.sos})}>
                    Strongness of support
                </Button>
                <Button
                    type="submit"
                    variant={filter.rw === true ? "contained" : "outlined"}
                    sx={{
                        m: 1,
                    }}
                    onClick={() => setFilter({...filter, rw: !filter.rw})}>
                    Reverse Weightage
                </Button>
                <Button
                    type="submit"
                    variant={filter.bs === true ? "contained" : "outlined"}
                    sx={{
                        m: 1,
                    }}
                    onClick={() => setFilter({...filter, bs: !filter.bs})}>
                    Buy/Sell
                </Button>
                <Button
                    type="submit"
                    variant={filter.sl === true ? "contained" : "outlined"}
                    sx={{
                        m: 1,
                    }}
                    onClick={() => setFilter({...filter, sl: !filter.sl})}>
                    Strongness Level
                </Button>
                <Button
                    type="submit"
                    variant={filter.is === true ? "contained" : "outlined"}
                    sx={{
                        m: 1,
                    }}
                    onClick={() => setFilter({...filter, is: !filter.is})}>
                    Immediate Support
                </Button>
                <Button
                    type="submit"
                    variant={filter.ss === true ? "contained" : "outlined"}
                    sx={{
                        m: 1,
                    }}
                    onClick={() => setFilter({...filter, ss: !filter.ss})}>
                    Strong Support
                </Button>
                <Button
                    type="submit"
                    variant={filter.pcrw === true ? "contained" : "outlined"}
                    sx={{
                        m: 1,
                    }}
                    onClick={() => setFilter({...filter, pcrw: !filter.pcrw})}>
                    PCR Weightage
                </Button>
                <Button
                    type="submit"
                    variant={filter.cprw === true ? "contained" : "outlined"}
                    sx={{
                        m: 1,
                    }}
                    onClick={() => setFilter({...filter, cprw: !filter.cprw})}>
                    CPR Weightage
                </Button>
            </Box>
        </Box>
    )
}

export default HandleOptions;