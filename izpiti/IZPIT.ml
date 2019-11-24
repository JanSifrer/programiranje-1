(* =================== *)
(* 1. naloga: funkcije *)
(* =================== *)

let is_root x y =
    if x < 0  then false else
        if x*x = y then true else false

let pack3 a b c =
    (a, b, c)

let sum_if_not f list =
    let rec sum' f list acc =
        match list with
        | [] -> acc
        | x :: xs -> if f x then (sum' f xs acc) else (sum' f xs (x + acc))
    in
    sum' f list 0

(*let apply flist list=
    let rec apply' flist list acc =
        match list with
        | [] -> acc
        | x :: xs -> 
        let ys = y :: ys in 
            apply' xs ys (y x :: acc) 
        in
    apply' flist list []*)
    

(* ======================================= *)
(* 2. naloga: podatkovni tipi in rekurzija *)
(* ======================================= *)

type vrsta_srecanja =
    | Predavanja
    | Vaje

type srecanje = {predmet : string; vrsta : vrsta_srecanja; trajanje : int}

type urnik = {dan : int; srecanje : srecanje}

let vaje = {predmet = "Analiza 2a"; vrsta = Vaje; trajanje = 2}

let predavanje = {predmet = "Programiranje 1"; vrsta = Predavanja; trajanje = 2}

let urnik_profesor = 
    {dan = 1; srecanje = {predmet = "Analiza 2a"; vrsta = Vaje; trajanje = 2}},
    {dan = 3; srecanje = {predmet = "Analiza 2a"; vrsta = Predavanja; trajanje = 1}},
    {dan = 6; srecanje = {predmet = "Analiza 2a"; vrsta = Vaje; trajanje = 1}}


let je_preobremenjen srecanje =
    if srecanje.dan = 6 then false else true

let bogastvo () = failwith "dopolni me"