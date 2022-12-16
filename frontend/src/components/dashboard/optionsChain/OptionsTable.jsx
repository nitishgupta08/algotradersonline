import {styled, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography, Box} from "@mui/material";
import React from "react";
import {useTheme} from "@mui/material/styles";

const OptionsTable = ({data, filter, spot, bold, fsize}) => {
    const theme = useTheme();
    const HeadTableCell = styled(TableCell)(() => ({
        borderWidth: 0.1,
        borderRightWidth: 1,
        borderBottomWidth: 1,
        borderColor:
            theme.palette.mode === "dark" ? "text.primary" : "rgba(0, 0, 0, 0.2)",
        borderStyle: "solid",
    }));

    // Only get 10 prices above and below spot price
    if(data && data.length > 0) {
        data = data.filter((obj) => {
            return Math.abs(obj['Strike_Price'] - spot) <= 500
        })
    }

    let temp = data && data.slice(); //slice() returns a new array
    let arr = [];

    if (data && data.length > 0) {
        temp.sort((a, b) => {
            return b["OI_C"] - a["OI_C"];
        });
        arr[0] = [temp[0]["OI_C"], temp[1]["OI_C"]];

        temp.sort((a, b) => {
            return b["OI_Change_C"] - a["OI_Change-C"];
        });
        arr[1] = [temp[0]["OI_Change_C"], temp[1]["OI_Change_C"]];

        temp.sort((a, b) => {
            return b["Volume_C"] - a["Volume_C"];
        });
        arr[2] = [temp[0]["Volume_C"] , temp[1]["Volume_C"]];

        temp.sort((a, b) => {
            return b["OI_P"] - a["OI_P"];
        });
        arr[3] = [temp[0]["OI_P"], temp[1]["OI_P"]];

        temp.sort((a, b) => {
            return b["OI_Change_P"] - a["OI_Change-P"];
        });
        arr[4] = [temp[0]["OI_Change_P"], temp[1]["OI_Change_P"]];

        temp.sort((a, b) => {
            return b["Volume_P"] - a["Volume_P"];
        });
        arr[5] = [temp[0]["Volume_P"] , temp[1]["Volume_P"]];
    }

    return (
        <>
            {data ? (data.length > 0 ? (
            <TableContainer sx={{width: "100%", mt: 2, pl: 2, pr: 2}}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell
                                colSpan={4}
                                align="center"
                                sx={{backgroundColor: "green "}}>
                                <Typography
                                    variant="subtitle"
                                    sx={{
                                        fontSize: "1rem",
                                        fontWeight: "600",
                                        color: "white",
                                    }}>
                                    CALLS
                                </Typography>
                            </TableCell>
                            <TableCell
                                align="center"
                                rowSpan={2}
                                sx={{
                                    borderWidth: 0.1,
                                    borderRightWidth: 1,
                                    borderBottomWidth: 1,
                                    backgroundColor:
                                        theme.palette.mode === "dark" ? "rgb(224,211,120)" : "rgb(224,211,120)",
                                    borderColor:
                                        theme.palette.mode === "dark"
                                            ? "text.primary"
                                            : "rgba(0, 0, 0, 0.2)",
                                    borderStyle: "solid",
                                }}>
                                <Typography
                                    variant="subtitle"
                                    sx={{fontSize: "1rem", fontWeight: 600}}>
                                    STRIKE PRICE
                                </Typography>
                            </TableCell>
                            <TableCell
                                colSpan={4}
                                align="center"
                                sx={{backgroundColor: "red"}}>
                                <Typography
                                    variant="subtitle"
                                    sx={{
                                        fontSize: "1rem",
                                        fontWeight: "600",
                                        color: "white",
                                    }}>
                                    PUTS
                                </Typography>
                            </TableCell>
                            {filter.pcoc && (<TableCell
                                align="center"
                                rowSpan={2}
                                sx={{
                                    borderWidth: 0.1,
                                    borderRightWidth: 1,
                                    borderBottomWidth: 1,
                                    backgroundColor:
                                        theme.palette.mode === "dark" ? "rgb(224,211,120)" : "rgb(224,211,120)",

                                    borderColor:
                                        theme.palette.mode === "dark"
                                            ? "text.primary"
                                            : "rgba(0, 0, 0, 0.2)",
                                    borderStyle: "solid",
                                }}>
                                <Typography
                                    variant="subtitle"
                                    sx={{fontSize: "1rem", fontWeight: 600}}>
                                    PUT-CALL OI CHNG
                                </Typography>
                            </TableCell>)}
                            {filter.pco && (<TableCell
                                align="center"
                                rowSpan={2}
                                sx={{
                                    borderWidth: 0.1,
                                    borderRightWidth: 1,
                                    borderBottomWidth: 1,
                                    backgroundColor:
                                        theme.palette.mode === "dark" ? "rgb(224,211,120)" : "rgb(224,211,120)",

                                    borderColor:
                                        theme.palette.mode === "dark"
                                            ? "text.primary"
                                            : "rgba(0, 0, 0, 0.2)",
                                    borderStyle: "solid",
                                }}>
                                <Typography
                                    variant="subtitle"
                                    sx={{fontSize: "1rem", fontWeight: 600}}>
                                    PUT-CALL OI
                                </Typography>
                            </TableCell>)}
                            {filter.pcr && (<TableCell
                                align="center"
                                rowSpan={2}
                                sx={{
                                    borderWidth: 0.1,
                                    borderRightWidth: 1,
                                    borderBottomWidth: 1,
                                    backgroundColor:
                                        theme.palette.mode === "dark" ? "rgb(224,211,120)" : "rgb(224,211,120)",

                                    borderColor:
                                        theme.palette.mode === "dark"
                                            ? "text.primary"
                                            : "rgba(0, 0, 0, 0.2)",
                                    borderStyle: "solid",
                                }}>
                                <Typography
                                    variant="subtitle"
                                    sx={{fontSize: "1rem", fontWeight: 600}}>
                                    PCR
                                </Typography>
                            </TableCell>)}
                            {filter.cpr && (<TableCell
                                align="center"
                                rowSpan={2}
                                sx={{
                                    borderWidth: 0.1,
                                    borderRightWidth: 1,
                                    borderBottomWidth: 1,
                                    backgroundColor:
                                        theme.palette.mode === "dark" ? "rgb(224,211,120)" : "rgb(224,211,120)",

                                    borderColor:
                                        theme.palette.mode === "dark"
                                            ? "text.primary"
                                            : "rgba(0, 0, 0, 0.2)",
                                    borderStyle: "solid",
                                }}>
                                <Typography
                                    variant="subtitle"
                                    sx={{fontSize: "1rem", fontWeight: 600}}>
                                    CPR
                                </Typography>
                            </TableCell>)}
                            {filter.sos && (<TableCell
                                align="center"
                                rowSpan={2}
                                sx={{
                                    borderWidth: 0.1,
                                    borderRightWidth: 1,
                                    borderBottomWidth: 1,
                                    backgroundColor:
                                        theme.palette.mode === "dark" ? "rgb(224,211,120)" : "rgb(224,211,120)",

                                    borderColor:
                                        theme.palette.mode === "dark"
                                            ? "text.primary"
                                            : "rgba(0, 0, 0, 0.2)",
                                    borderStyle: "solid",
                                }}>
                                <Typography
                                    variant="subtitle"
                                    sx={{fontSize: "1rem", fontWeight: 600}}>
                                    Strongness of Support
                                </Typography>
                            </TableCell>)}
                            {filter.rw && (<TableCell
                                align="center"
                                rowSpan={2}
                                sx={{
                                    borderWidth: 0.1,
                                    borderRightWidth: 1,
                                    borderBottomWidth: 1,
                                    backgroundColor:
                                        theme.palette.mode === "dark" ? "rgb(224,211,120)" : "rgb(224,211,120)",

                                    borderColor:
                                        theme.palette.mode === "dark"
                                            ? "text.primary"
                                            : "rgba(0, 0, 0, 0.2)",
                                    borderStyle: "solid",
                                }}>
                                <Typography
                                    variant="subtitle"
                                    sx={{fontSize: "1rem", fontWeight: 600}}>
                                    Reverse Weightage
                                </Typography>
                            </TableCell>)}
                            {filter.bs && (<TableCell
                                align="center"
                                rowSpan={2}
                                sx={{
                                    borderWidth: 0.1,
                                    borderRightWidth: 1,
                                    borderBottomWidth: 1,
                                    backgroundColor:
                                        theme.palette.mode === "dark" ? "rgb(224,211,120)" : "rgb(224,211,120)",

                                    borderColor:
                                        theme.palette.mode === "dark"
                                            ? "text.primary"
                                            : "rgba(0, 0, 0, 0.2)",
                                    borderStyle: "solid",
                                }}>
                                <Typography
                                    variant="subtitle"
                                    sx={{fontSize: "1rem", fontWeight: 600}}>
                                    Buy/Sell
                                </Typography>
                            </TableCell>)}
                            {filter.sl && (<TableCell
                                align="center"
                                rowSpan={2}
                                sx={{
                                    borderWidth: 0.1,
                                    borderRightWidth: 1,
                                    borderBottomWidth: 1,
                                    backgroundColor:
                                        theme.palette.mode === "dark" ? "rgb(224,211,120)" : "rgb(224,211,120)",

                                    borderColor:
                                        theme.palette.mode === "dark"
                                            ? "text.primary"
                                            : "rgba(0, 0, 0, 0.2)",
                                    borderStyle: "solid",
                                }}>
                                <Typography
                                    variant="subtitle"
                                    sx={{fontSize: "1rem", fontWeight: 600}}>
                                    Strongness Level
                                </Typography>
                            </TableCell>)}
                            {filter.is && (<TableCell
                                align="center"
                                rowSpan={2}
                                sx={{
                                    borderWidth: 0.1,
                                    borderRightWidth: 1,
                                    borderBottomWidth: 1,
                                    backgroundColor:
                                        theme.palette.mode === "dark" ? "rgb(224,211,120)" : "rgb(224,211,120)",

                                    borderColor:
                                        theme.palette.mode === "dark"
                                            ? "text.primary"
                                            : "rgba(0, 0, 0, 0.2)",
                                    borderStyle: "solid",
                                }}>
                                <Typography
                                    variant="subtitle"
                                    sx={{fontSize: "1rem", fontWeight: 600}}>
                                    Immediate Support
                                </Typography>
                            </TableCell>)}
                            {filter.ss && (<TableCell
                                align="center"
                                rowSpan={2}
                                sx={{
                                    borderWidth: 0.1,
                                    borderRightWidth: 1,
                                    borderBottomWidth: 1,
                                    backgroundColor:
                                        theme.palette.mode === "dark" ? "rgb(224,211,120)" : "rgb(224,211,120)",

                                    borderColor:
                                        theme.palette.mode === "dark"
                                            ? "text.primary"
                                            : "rgba(0, 0, 0, 0.2)",
                                    borderStyle: "solid",
                                }}>
                                <Typography
                                    variant="subtitle"
                                    sx={{fontSize: "1rem", fontWeight: 600}}>
                                    Strong Support
                                </Typography>
                            </TableCell>)}
                            {filter.pcrw && (<TableCell
                                align="center"
                                rowSpan={2}
                                sx={{
                                    borderWidth: 0.1,
                                    borderRightWidth: 1,
                                    borderBottomWidth: 1,
                                    backgroundColor:
                                        theme.palette.mode === "dark" ? "rgb(224,211,120)" : "rgb(224,211,120)",

                                    borderColor:
                                        theme.palette.mode === "dark"
                                            ? "text.primary"
                                            : "rgba(0, 0, 0, 0.2)",
                                    borderStyle: "solid",
                                }}>
                                <Typography
                                    variant="subtitle"
                                    sx={{fontSize: "1rem", fontWeight: 600}}>
                                    PCR Weightage
                                </Typography>
                            </TableCell>)}
                            {filter.cprw && (<TableCell
                                align="center"
                                rowSpan={2}
                                sx={{
                                    borderWidth: 0.1,
                                    borderRightWidth: 1,
                                    borderBottomWidth: 1,
                                    backgroundColor:
                                        theme.palette.mode === "dark" ? "rgb(224,211,120)" : "rgb(224,211,120)",

                                    borderColor:
                                        theme.palette.mode === "dark"
                                            ? "text.primary"
                                            : "rgba(0, 0, 0, 0.2)",
                                    borderStyle: "solid",
                                }}>
                                <Typography
                                    variant="subtitle"
                                    sx={{fontSize: "1rem", fontWeight: 600}}>
                                    CPR Weightage
                                </Typography>
                            </TableCell>)}
                        </TableRow>
                        <TableRow>
                            <HeadTableCell align="center">
                                <Typography
                                    variant="subtitle"
                                    sx={{
                                        fontSize: "1rem",
                                        fontWeight: "600",
                                    }}>
                                    OI
                                </Typography>
                            </HeadTableCell>

                            <HeadTableCell align="center">
                                <Typography
                                    variant="subtitle"
                                    sx={{
                                        fontSize: "1rem",
                                        fontWeight: "600",
                                    }}>
                                    CHNG IN OI
                                </Typography>
                            </HeadTableCell>

                            <HeadTableCell align="center">
                                <Typography
                                    variant="subtitle"
                                    sx={{
                                        fontSize: "1rem",
                                        fontWeight: "600",
                                    }}>
                                    VOL
                                </Typography>
                            </HeadTableCell>


                            <HeadTableCell align="center">
                                <Typography
                                    variant="subtitle"
                                    sx={{
                                        fontSize: "1rem",
                                        fontWeight: "600",
                                    }}>
                                    LTP
                                </Typography>
                            </HeadTableCell>


                            <HeadTableCell align="center">
                                <Typography
                                    variant="subtitle"
                                    sx={{
                                        fontSize: "1rem",
                                        fontWeight: "600",
                                    }}>
                                    LTP
                                </Typography>
                            </HeadTableCell>

                            <HeadTableCell align="center">
                                <Typography
                                    variant="subtitle"
                                    sx={{
                                        fontSize: "1rem",
                                        fontWeight: "600",
                                    }}>
                                    VOL
                                </Typography>
                            </HeadTableCell>

                            <HeadTableCell align="center">
                                <Typography
                                    variant="subtitle"
                                    sx={{
                                        fontSize: "1rem",
                                        fontWeight: "600",
                                    }}>
                                    CHNG IN OI
                                </Typography>
                            </HeadTableCell>
                            <HeadTableCell align="center">
                                <Typography
                                    variant="subtitle"
                                    sx={{
                                        fontSize: "1rem",
                                        fontWeight: "600",
                                    }}>
                                    OI
                                </Typography>
                            </HeadTableCell>
                        </TableRow>
                    </TableHead>
                        <TableBody>
                            {data.map((row, id) => {
                                return (
                                    <StrikeRow
                                        key={id}
                                        row={row}
                                        filter={filter}
                                        spot={spot}
                                        theme={theme}
                                        arr={arr}
                                        bold={bold}
                                        fsize={fsize}
                                    />
                                );
                            })
                        }
                        </TableBody>
                </Table>
            </TableContainer>) : (
                <Box
                    component="img"
                    sx={{
                        height: 500,
                        ml:"35%"
                    }}
                    alt="The house from the offer."
                    src="/no_data.png"
                />

            )):null}

        </>
    )
};

const StrikeRow = ({row, filter, spot, theme, arr, bold,fsize}) => {
    const StyledTableCell = styled(TableCell)(({ theme, ce,pe}) => ({
        backgroundColor:
            row["Strike_Price"] === spot
                ? "rgb(224,211,120)"
                : (ce === 1 ? row["Strike_Price"] < spot :(pe === 1 ? row["Strike_Price"] > spot : false))
                    ? "#B5DEFF"
                    : "background.paper",
        borderWidth: 0.1,
        textAlign:"center",
        fontWeight: row["Strike_Price"] === spot ? "600" : bold ? 700 : 500,
        borderColor:
            theme.palette.mode === "dark" ? "rgba(255,255,255,1)" : "rgba(0,0,0,0.2)",
        borderStyle: "solid",
        fontSize:`${fsize}rem`
    }));
    return (
        <TableRow key={row["Strike_Price"]}>
            <StyledTableCell ce={1} sx={{
                backgroundColor:
                    row["OI_C"] === arr[0][0]
                        ? "#FFD700"
                        : row["OI_C"] === arr[0][1]
                            ? "#C0C0C0"
                            : null,
            }}>
                {row["OI_C"].toLocaleString()}
            </StyledTableCell>
            <StyledTableCell ce={1} sx={{
                color:row["OI_Change_C"]>0?"green":"red",
                backgroundColor:
                    row["OI_Change_C"] === arr[1][0]
                        ? "#FFD700"
                        : row["OI_Change_C"] === arr[1][1]
                            ? "#C0C0C0"
                            : null,
            }}>
                {row["OI_Change_C"].toLocaleString()}
            </StyledTableCell>
            <StyledTableCell ce={1} sx={{
                backgroundColor:
                    row["Volume_C"] === arr[2][0]
                        ? "#FFD700"
                        : row["Volume_C"] === arr[2][1]
                            ? "#C0C0C0"
                            : null,
            }}>
                {row["Volume_C"].toLocaleString()}
            </StyledTableCell>
            <StyledTableCell ce={1}>
                {row["LTP_C"] ? row["LTP_C"].toFixed(2) : "-"}
            </StyledTableCell>
            <StyledTableCell
                sx={{
                    backgroundColor:
                        theme.palette.mode === "dark" ? "rgb(68,65,42)" : "rgb(224,211,120)",
                    borderWidth: 0,
                    borderRightWidth: 1,
                    borderBottomWidth: 1,
                    fontWeight: 600,
                    borderColor:
                        theme.palette.mode === "dark"
                            ? "text.primary"
                            : "rgba(0, 0, 0, 0.2)",
                    borderStyle: "solid",
                    color:"darkblue"
                }}
            >
                {row["Strike_Price"].toLocaleString("en-IN", {
                    maximumFractionDigits: 0,
                    style: "currency",
                    currency: "INR",
                })}
            </StyledTableCell>
            <StyledTableCell pe={1}>
                {row["LTP_P"] ? row["LTP_P"].toFixed(2) : "-"}
            </StyledTableCell>
            <StyledTableCell pe={1} sx={{
                backgroundColor:
                    row["Volume_P"] === arr[5][0]
                        ? "#FFD700"
                        : row["Volume_P"] === arr[5][1]
                            ? "#C0C0C0"
                            : null,
            }}>
                {row["Volume_P"].toLocaleString()}
            </StyledTableCell>
            <StyledTableCell pe={1} sx={{
                color:row["OI_Change_P"]>0?"green":"red",
                backgroundColor:
                    row["OI_Change_P"] === arr[4][0]
                        ? "#FFD700"
                        : row["OI_Change_P"]=== arr[4][1]
                            ? "#C0C0C0"
                            : null,
            }}>
                {row["OI_Change_P"].toLocaleString()}
            </StyledTableCell>
            <StyledTableCell pe={1} sx={{
                backgroundColor:
                    row["OI_P"] === arr[3][0]
                        ? "#FFD700"
                        : row["OI_P"] === arr[3][1]
                            ? "#C0C0C0"
                            : null,
            }}>
                {row["OI_P"].toLocaleString()}
            </StyledTableCell>
            {filter.pcoc && (<StyledTableCell sx={{color:row["PUT_CALL_OI_CHN"]>0?"green":"red"}}>
                {row["PUT_CALL_OI_CHN"].toLocaleString()}
            </StyledTableCell>)}
            {filter.pco && (<StyledTableCell sx={{color:row["PUT_CALL_OI"]>0?"green":"red"}}>
                {row["PUT_CALL_OI"].toLocaleString()}
            </StyledTableCell>)}
            {filter.pcr && (<StyledTableCell>
                {row["PCR"] ? row["PCR"].toFixed(2) : "-"}
            </StyledTableCell>)}
            {filter.cpr && (<StyledTableCell>
                {row["CPR"] ? row["CPR"].toFixed(2) : "-"}
            </StyledTableCell>)}
            {filter.sos && (<StyledTableCell sx={{color:row["STRONGNESS_OF_SUPPORT"]>0?"green":"red"}}>
                {row["STRONGNESS_OF_SUPPORT"] ? row["STRONGNESS_OF_SUPPORT"].toFixed(2) : "-"}
            </StyledTableCell>)}
            {filter.rw && (<StyledTableCell sx={{color:row["Reverse_Weightage"]>0?"green":"red"}}>
                {row["Reverse_Weightage"] ? row["Reverse_Weightage"].toFixed(2) : "-"}
            </StyledTableCell>)}
            {filter.bs && (<StyledTableCell>
                {row["Buy_Sell"]}
            </StyledTableCell>)}
            {filter.sl && (<StyledTableCell>
                {row["Stongness_Level"]}
            </StyledTableCell>)}
            {filter.is && (<StyledTableCell>
                {row["Immediate_Support"] ? row["Immediate_Support"].toLocaleString() : "-"}
            </StyledTableCell>)}
            {filter.ss && (<StyledTableCell>
                {row["Strong_Support"] ? row["Strong_Support"].toLocaleString() : "-"}
            </StyledTableCell>)}
            {filter.pcrw && (<StyledTableCell sx={{color:row["PCR_Weightage"]>0?"green":row["PCR_Weightage"] && "red"}}>
                {row["PCR_Weightage"] ? row["PCR_Weightage"].toLocaleString() : "-"}
            </StyledTableCell>)}
            {filter.cprw && (<StyledTableCell sx={{color:row["CPR_Weightage"]>0?"green":row["CPR_Weightage"] && "red"}}>
                {row["CPR_Weightage"] ? row["CPR_Weightage"].toLocaleString() : "-"}
            </StyledTableCell>)}
        </TableRow>
    );
}


export default OptionsTable;