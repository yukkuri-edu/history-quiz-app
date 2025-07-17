from flask import Flask, request, render_template, session, redirect, url_for
import random # 問題のシャッフルなどで使用

app = Flask(__name__)
app.secret_key = "your_very_secret_key_here" # ★本番環境ではより複雑な文字列に変更してください★

# --- クイズデータ構造の変更 ---
# テーマごとに問題をまとめる辞書形式に変更します。
# 各テーマの中に、問題IDと問題の詳細データを持つ構造になります。
quiz_themes = {
    "土地制度史": {
        1: {
            "question": "【土地制度史】743年に出された、土地の私有を認めた法令は何でしょう？",
            "choices": {"A": "班田収授法", "B": "墾田永年私財法", "C": "三世一身法", "D": "荘園整理令"},
            "correct_answer": "B",
            "explanation": "墾田永年私財法によって土地の私有が認められました。 律令制の下では人々には口分田が与えられ、死んだら口分田を返すという公地公民制が採られていた。公地公民制の運用は、班田収授法によって行われた。奈良時代には、口分田が不足するようになり、723年に三世一身法が、743年に墾田永年私財法が出され新たに田を開墾することや昔からの田を整備することが促された。墾田永年私財法が出された結果、力のある貴族や寺社は、逃亡してきた農民をつかい私有地である荘園を拡げていった。"
        },
        2: {
            "question": "【土地制度史】源頼朝が朝廷に認めさせて、荘園や公領ごとに置かれた役職は何でしょう？",
            "choices": {"A": "守護", "B": "五人組", "C": "地頭", "D": "問注所"},
            "correct_answer": "C",
            "explanation": "鎌倉幕府の初代将軍となる源頼朝は朝廷に、国ごとに守護を、荘園や公領ごとに地頭を置くことを認めさせて勢力を拡大した。武士は荘園において地頭として農民を支配していた。しばしば、地頭と荘園を所有する荘園領主との間では争いが起こったが、地頭が農民からの年貢取り立てを一手に引き受けるようになるなど、地頭の力は増していった。その他の選択肢である問注所は鎌倉幕府の裁判機関であり、五人組は江戸時代に農村で年貢の納入などに連帯責任を負わせた制度のこと。"
        },
        3: {
            "question": "【土地制度史】戦国大名は自分の領国を富ませるために農村の治水や灌がいを進めた。戦国大名が領国を支配するために定めた法律を何というでしょう？",
            "choices": {"A": "武家諸法度", "B": "公地公民", "C": "分国法", "D": "楽市楽座"},
            "correct_answer": "C",
            "explanation": "戦国大名は、古くからの勢力を抑え領地を独立して支配した。領地の支配を徹底するために分国法と呼ばれる法律も定めていた。楽市楽座は織田信長が城下町で商工業を発展させるために採った政策のこと。公地公民は、飛鳥時代・奈良時代の律令制で土地と人民は天皇のものであったこと。律令制では、人民に口分田が与えられた。武家諸法度は江戸時代に定められた、大名を統制するための法律。"
        },
        4: {
            "question": "【土地制度史】太閤検地を行った人物は誰でしょう？",
            "choices": {"A": "織田信長", "B": "徳川家康", "C": "豊臣秀吉", "D": "足利義満"},
            "correct_answer": "C",
            "explanation": "豊臣秀吉が行った検地を太閤検地という。太閤検地ではものさしやますが統一され、全国の田畑の予想される収穫量が実地で把握された。これにより、荘園領主や有力農民が持っていた、複雑な土地の支配関係が否定された。"
        },
        5: {
            "question": "【土地制度史】明治政府が農民の土地所有権を認める一方で、地価の3%の税金を現金で納めさせるようにしたことを何というでしょう？",
            "choices": {"A": "地租改正", "B": "版籍奉還", "C": "農地改革", "D": "廃藩置県"},
            "correct_answer": "A",
            "explanation": "明治初期においても、、"
        }
        # さらに土地制度史の問題を追加できます
    },
    "外交史": {
        1: {
            "question": "【外交史】聖徳太子は、隋との対等の外交を目指し、小野妹子らを派遣した。この使節を何というでしょう？",
            "choices": {"A": "朝鮮通信使", "B": "大宰府", "C": "防人", "D": "遣隋使"},
            "correct_answer": "D",
            "explanation": "聖徳太子は、遣隋使として小野妹子らを隋へ派遣した。遣隋使には、留学生や学問僧らも従っており、後に帰国し国づくりに貢献した。防人は、九州の警護にあたる兵役のこと。7世紀に白村江の戦いで、日本が唐軍に敗れたため九州の警護が強められた。九州には外交・国防上の要地として大宰府が置かれた。朝鮮通信使は、江戸時代に将軍の代替わりのたびに、朝鮮から派遣された外交使節。"
        },
        2: {
            "question": "【外交史】平清盛が日宋貿易の拠点として整備した大和田の泊は現在の何市にあったでしょう？",
            "choices": {"A": "神戸市", "B": "長崎市", "C": "那覇市", "D": "横浜市"},
            "correct_answer": "A",
            "explanation": "平安時代末期になると武士が力を持つようになってきた。平清盛は、藤原氏のように天皇の外戚となって権力を握った。日宋貿易にも力を入れ、大和田の泊（現在の神戸市）を整備した。瀬戸内海の航路を安全にたもち、宋の商人を招き入れ貿易を推進した。"
        },
        3: {
            "question": "【外交史】鎌倉時代、モンゴル帝国に出自をもつフビライハンが、日本を2度、襲来したことを何というでしょう？",
            "choices": {"A": "壇ノ浦の戦い", "B": "元寇", "C": "承久の乱", "D": "平治の乱"},
            "correct_answer": "B",
            "explanation": "解説3"
        },
        4: {
            "question": "【外交史】鎖国を行った江戸幕府が唯一公認した貿易港はどこでしょう？",
            "choices": {"A": "堺", "B": "博多", "C": "長崎", "D": "那覇"},
            "correct_answer": "C",
            "explanation": "解説3"
        },
        5: {
            "question": "【外交史】ペリーが浦賀に来航した年は西暦何年でしょう？",
            "choices": {"A": "1853年", "B": "1868年", "C": "1871年", "D": "1894年"},
            "correct_answer": "A",
            "explanation": "解説4"
        }
    },        # さらに外交史の問題を追加できます
    "文化史": {
        1: {
            "question": "【文化史】源氏物語の作者は誰でしょう？",
            "choices": {"A": "清少納言", "B": "紫式部", "C": "小野小町", "D": "和泉式部"},
            "correct_answer": "B",
            "explanation": "解説5"
        },
        2: {
            "question": "【文化史】金閣寺を建立した人物は誰でしょう？",
            "choices": {"A": "足利義満", "B": "足利義政", "C": "豊臣秀吉", "D": "徳川家康"},
            "correct_answer": "A",
            "explanation": "解説6"
        }
        # さらに文化史の問題を追加できます
    }
}

@app.route("/")
def index():
    # クイズのトップページ。テーマ選択肢を渡す
    themes = list(quiz_themes.keys()) # 利用可能なテーマのリスト
    return render_template("quiz.html", themes=themes, show_theme_selection=True)

@app.route("/start_quiz", methods=["POST"])
def start_quiz():
    # ユーザーが選択したテーマを取得
    selected_theme = request.form.get("theme")

    if selected_theme not in quiz_themes:
        # 無効なテーマが選択された場合はエラーまたはトップに戻す
        return redirect(url_for('index'))

    # セッションを初期化し、選択されたテーマと問題リストを設定
    session.clear()
    session['selected_theme'] = selected_theme
    # 選択されたテーマの問題を取得し、順番をシャッフル（オプション）
    session['question_ids'] = list(quiz_themes[selected_theme].keys())
    random.shuffle(session['question_ids']) # 問題をランダムにする
    
    session['current_question_index'] = 0 # 現在の問題のインデックス
    session['score'] = 0 # スコアを初期化
    session['quiz_started'] = True # クイズ開始フラグ

    # 最初の問題の表示にリダイレクト
    return redirect(url_for('show_question'))

@app.route("/question")
def show_question():
    if 'quiz_started' not in session or not session['quiz_started']:
        return redirect(url_for('index')) # クイズが始まっていない場合はテーマ選択に戻す

    selected_theme = session.get('selected_theme')
    question_ids = session.get('question_ids')
    current_question_index = session.get('current_question_index')

    if not selected_theme or not question_ids or current_question_index is None:
        return redirect(url_for('index')) # セッション情報が不正ならトップに戻す

    # 現在の問題IDを取得
    question_id = question_ids[current_question_index]
    question = quiz_themes[selected_theme].get(question_id)
    #explanation = session.get(question)

    if not question:
        # 問題が見つからない場合はエラーページなどにリダイレクト
        session.clear()
        return redirect(url_for('index'))

    return render_template(
        "quiz.html",
        question_data=question,
        #explanation_data=explanation,
        question_number=current_question_index + 1, # ユーザー向けに1から表示
        total_questions=len(question_ids), # 総問題数を表示
        show_result_on_question=False,
        show_next_button=False,
        show_final_result_button=False,
        show_theme_selection=False # 問題表示中はテーマ選択を表示しない
    )

@app.route("/answer", methods=["POST"])
def process_answer():
    if 'quiz_started' not in session or not session['quiz_started']:
        return redirect(url_for('index'))

    user_answer = request.form.get("user_answer")
    selected_theme = session.get('selected_theme')
    question_ids = session.get('question_ids')
    current_question_index = session.get('current_question_index')
    
    if not selected_theme or not question_ids or current_question_index is None or not user_answer:
        return redirect(url_for('index'))

    question_id = question_ids[current_question_index]
    question = quiz_themes[selected_theme].get(question_id)
    explanation = question["explanation"]

    if not question:
        session.clear()
        return redirect(url_for('index'))

    is_correct = (user_answer == question["correct_answer"])

    if is_correct:
        session['score'] = session.get('score', 0) + 1

    # 次の問題のインデックスを計算
    next_question_index = current_question_index + 1

    render_params = {
        "question_data": question,
        "explanation_data": explanation,
        "question_number": current_question_index + 1,
        "total_questions": len(question_ids),
        "user_answered": user_answer,
        "is_correct": is_correct,
        #"explanation_data": explanation,
        "show_result_on_question": True, # 正誤判定を表示
        "show_next_button": False,
        "show_final_result_button": False,
        "show_theme_selection": False # 問題表示中はテーマ選択を表示しない
    }

    if next_question_index < len(question_ids):
        session['current_question_index'] = next_question_index
        render_params["show_next_button"] = True
    else:
        render_params["show_final_result_button"] = True

    return render_template("quiz.html", **render_params)

@app.route("/final_result")
def show_final_result():
    final_score = session.get('score', 0)
    selected_theme = session.get('selected_theme')
    total_questions = len(session.get('question_ids', [])) if session.get('question_ids') else 0
    session.clear() # クイズ終了なのでセッションデータをクリア

    return render_template(
        "final_result.html",
        final_score=final_score,
        total_questions=total_questions,
        selected_theme=selected_theme
    )

if __name__ == "__main__":
    app.run(debug=True)